from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseNotFound
from post.templatetags.post_filters import *
from .models import *

# Create your views here.

class HomeView(ListView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            all_posts = []
            for following in self.request.user.userprofile.follows.all():
                all_posts += following.owner.posts.all().order_by('-creation_date')[:10]
            
            return sorted(all_posts, key = lambda each_post: each_post.creation_date, reverse = True)

    def get_template_names(self):
        '''
        Returns different template for homepage based on if user is authenticated or not.
        '''
        if self.request.user.is_authenticated:
            return 'post/signed_in_home.html'
        else:
            return 'userprofile/not_signed_in_home.html'


class ProfileView(LoginRequiredMixin, TemplateView):
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


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        
        try:
            context['image_name'] = 'r' + str(self.object.postreactions.get(reactor = self.request.user).reaction)
        except Reaction.DoesNotExist:
            context['image_name'] = 'all'
        
        return context


class ReactionView(LoginRequiredMixin, View):
    http_method_names = ['get',]

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            post_id = request.GET.get('post_id', None)
            reaction_number = request.GET.get('reaction_number', None)

            if post_id == None or reaction_number == None:
                data = {
                    'success': False,
                }
            else:
                post = Post.objects.get(id = post_id)
                reaction, created = Reaction.objects.update_or_create(post = post, reactor = request.user, defaults = {'reaction': int(reaction_number)})

                data = {
                    'success': True,
                    'reactions': modify(post.postreactions.count()),
                    'plural': 's' if (post.postreactions.count() > 1) else '',
                }

            return JsonResponse(data)
        else:
            return HttpResponseNotFound()


class CommentView(LoginRequiredMixin, View):
    pass 
