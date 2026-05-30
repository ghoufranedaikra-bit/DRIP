from django.urls import path
from .views import ComplaintCreateView

urlpatterns = [
    path('', ComplaintCreateView.as_view()),
]