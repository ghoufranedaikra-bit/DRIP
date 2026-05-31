from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
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

        for item in items:
            if item.product.stock < item.quantity:
                return Response({
                    'error': f'Sorry, only {item.product.stock} units of "{item.product.name}" are available.'
                }, status=400)

        order = Order.objects.create(user=request.user)
        total = 0
        items_text = ''

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.stock -= item.quantity
            item.product.save()
            total += item.product.price * item.quantity
            items_text += f"\n- {item.product.name} x{item.quantity} — {item.product.price} DA"

        cart.cartitem_set.all().delete()

        if request.user.email:
            send_mail(
                subject=f'DRIP — Order #{order.id} Confirmed ✅',
                message=f'''Hey {request.user.username}!

Your order has been placed successfully 🔥

ORDER #{order.id}
{items_text}

Total: {total} DA
Payment: Cash on Delivery

We'll deliver your order soon. Pay when it arrives.

Stay fresh,
DRIP Team 🏷️''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)