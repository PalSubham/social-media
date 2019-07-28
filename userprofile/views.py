from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from .serializers import *

# Create your views here.

class SignInView(KnoxLoginView):

    permission_classes = (AllowAny,)

    def post(self, request, format = None):
        serializer = SignInSerializer(data = request.data, context = {'request': request,})
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        
        login(request, user)

        return super(SignInView, self).post(request, format)


class SignUpView(KnoxLoginView):

    permission_classes = (AllowAny,)

    def post(self, request, format = None):
        serializer = UserSerializer(data = request.data, context = {'request': request,})
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        login(request, user)

        return super(SignUpView, self).post(request, format)


class IsAuthenticatedView(APIView):

    permission_classes = (AllowAny,)
    authentication_classes = tuple()

    def get(self, request, *args, **kwargs):
        tokenauth = TokenAuthentication()
        
        try:
            user_token = tokenauth.authenticate(request)

            if user_token:
                user = user_token[0]
                serializer = UserSignedInSerializer(user)
                return Response(serializer.data)
            else:
                return Response({'signed_in': False})
        except AuthenticationFailed:
            return Response({'signed_in': False})


class ProfileViewSet(GenericViewSet):

    queryset = User.objects.all()

    def retrieve(self, request, pk = None):
        profile_user = self.get_object()
        userprofile = profile_user.userprofile

        profile_data = {
            'user': profile_user,
            'followings': userprofile.get_followings()[:8],
            'followers': userprofile.get_followers()[:8],
            'followings_no': userprofile.follows.count(),
            'followers_no': userprofile.followed_by.count(),
            'total_posts': profile_user.posts.count(),
        }
        serializer = ProfileSerializer(profile_data, context = {'request': request,})

        return Response(serializer.data)
