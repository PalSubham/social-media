from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('api/auth/signin/', SignInView.as_view(), name = 'signin'),
    path('api/auth/signup/', SignUpView.as_view(), name = 'signup'),
    path('api/', include(router.urls)),
]