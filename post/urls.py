from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('profile/', ProfileView.as_view(), name = 'profile'),
    path('details/<int:pk>/', PostDetailView.as_view(), name = 'postdetails'),
    path('reaction/', ReactionView.as_view(), name = 'reaction'),
    path('comment/', CommentView.as_view(), name = 'comment'),
    path('extra/', ExtraDataView.as_view(), name = 'extra'),
    path('createpost/', CreatePostView.as_view(), name = 'createpost'),
]

