from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import GraduateCreateView, VerifyOTP
urlpatterns = [
    path('create-graduate/', GraduateCreateView.as_view(), name='create-graduate'),
    path('verify/', VerifyOTP.as_view(), name='verify')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
