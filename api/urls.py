from django.urls import path
from .views import GraduateCreateView, VerifyOTP
urlpatterns = [
    path('create-graduate/', GraduateCreateView.as_view(), name='create-graduate'),
    path('verify/', VerifyOTP.as_view(), name='verify')
]
