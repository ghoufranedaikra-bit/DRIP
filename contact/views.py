from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from .models import Complaint
from .serializers import ComplaintSerializer

class ComplaintCreateView(generics.CreateAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def perform_create(self, serializer):
        complaint = serializer.save()

        send_mail(
            subject=f'DRIP — We received your message 📬',
            message=f'''Hey {complaint.name}!

We received your message and our team will get back to you within 24 hours.

YOUR MESSAGE:
Subject: {complaint.subject}
"{complaint.message}"

If it's urgent, reply to this email directly.

Stay fresh,
DRIP Support Team 🏷️''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[complaint.email],
            fail_silently=True,
        )

        send_mail(
            subject=f'New Complaint: {complaint.subject}',
            message=f'''New complaint received!

From: {complaint.name} ({complaint.email})
Subject: {complaint.subject}
Message: {complaint.message}''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=True,
        )