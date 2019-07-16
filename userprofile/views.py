from collections import namedtuple
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.viewsets import *
from .serializers import *
from .forms import *

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
        pass


class ProfileViewSet(GenericViewSet):

    Profile = namedtuple('Profile', ['user', 'followings', 'followers', 'followings_no', 'followers_no', 'total_posts',])
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

'''
class SignupView(FormView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        newuser = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(request = self.request, username = username, password = password)

        if not user == None:
            userprofile = user.userprofile
            userprofile.timezone = form.cleaned_data.get('timezone')
            userprofile.birthday = form.cleaned_data.get('birthday')
            userprofile.save()
            login(self.request, user)
        else:
            newuser.delete()

        return super(SignupView, self).form_valid(form)
'''