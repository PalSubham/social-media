from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('details/<int:pk>/', PostDetailView.as_view(), name = 'postdetails'),
]

