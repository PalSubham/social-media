from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from .models import *

# Create your views here.

class HomeView(ListView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter
            all_posts = []
            for following in self.request.user.userprofile.follows.all():
                all_posts = following.owner.posts.all().order_by('-creation_date')[:10]
            
            return sorted(all_posts, key = lambda each_post: each_post.creation_date, reverse = True)

    def get_template_names(self):
        '''
        Returns different template for homepage based on if user is authenticated or not.
        '''
        if self.request.user.is_authenticated:
            return 'post/signed_in_home.html'
        else:
            return 'userprofile/not_signed_in_home.html'


class ProfileView(TemplateView):
    template_name = 'post/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        userprofile = self.request.user.userprofile
        context['followings'] = userprofile.get_following()[:8]
        context['followers'] = userprofile.get_followers()[:8]
        context['posts'] = self.request.user.posts.all().order_by('-creation_date')
        context['follower_count'] = userprofile.followed_by.count()
        context['following_count'] = userprofile.follows.count()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_detail.html'