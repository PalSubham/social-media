from django.urls import path
from .views import *



urlpatterns = [
    path('api/feed/', FeedView.as_view(), name = 'feed'),
    path('api/postdetails/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name = 'postdetails'),
    path('api/createpost/', PostCreateView.as_view(), name = 'createpost'),
]

'''
    path('reaction/', ReactionView.as_view(), name = 'reaction'),
    path('comment/', CommentView.as_view(), name = 'comment'),
    path('extra/', ExtraDataView.as_view(), name = 'extra'),
    path('createpost/', CreatePostView.as_view(), name = 'createpost'),
    path('notifications/', NotificationView.as_view(), name = 'notifications'),
]
'''