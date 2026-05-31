from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(pre_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    if old_order.status == instance.status:
        return

    user = instance.user
    if not user.email:
        return

    status_messages = {
        'shipped': {
            'subject': f'DRIP — Your Order #{instance.id} Has Been Shipped! 🚚',
            'message': f'''Hey {user.username}!

Great news — your order is on its way! 🚚

ORDER #{instance.id} STATUS: SHIPPED

Your DRIP order has been picked up and is now on its way to you.
Get ready to receive your package soon!

Payment: Cash on Delivery — have your cash ready when it arrives.

If you have any questions, contact us at:
{settings.EMAIL_HOST_USER}

Stay fresh,
DRIP Team 🏷️'''
        },
        'delivered': {
            'subject': f'DRIP — Your Order #{instance.id} Has Been Delivered! ✅',
            'message': f'''Hey {user.username}!

Your order has been delivered! ✅

ORDER #{instance.id} STATUS: DELIVERED

We hope you love your new DRIP pieces! 🔥

Don't forget to:
- Pay the delivery person (Cash on Delivery)
- Share your fit on social media and tag us!

If anything is wrong with your order, contact us immediately:
{settings.EMAIL_HOST_USER}

Stay fresh,
DRIP Team 🏷️'''
        },
        'pending': {
            'subject': f'DRIP — Your Order #{instance.id} Is Being Processed',
            'message': f'''Hey {user.username}!

Your order #{instance.id} is currently being processed.
We will notify you as soon as it ships!

Stay fresh,
DRIP Team 🏷️'''
        }
    }

    email_data = status_messages.get(instance.status)
    if email_data:
        send_mail(
            subject=email_data['subject'],
            message=email_data['message'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )