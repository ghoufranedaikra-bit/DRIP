from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart

class OrderView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        cart = Cart.objects.get(user=request.user)
        items = cart.cartitem_set.all()

        if not items:
            return Response({'error': 'Cart is empty'}, status=400)

        order = Order.objects.create(user=request.user)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.cartitem_set.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data)