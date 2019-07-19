from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import *
from rest_framework.viewsets import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from notifications.models import *
from .models import *
from .serializers import *

# Create your views here.

class FeedView(ListAPIView):

    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        all_posts = []
        for following in self.request.user.userprofile.follows.all():
            all_posts += following.owner.posts.all().order_by('-creation_date')[:10]
        
        return sorted(all_posts, key = lambda each_post: each_post.creation_date, reverse = True)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer


'''class ReactionView(LoginRequiredMixin, View):
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            post_id = request.POST.get('post_id', None)
            reaction_number = request.POST.get('reaction_number', None)

            if post_id == None or reaction_number == None:
                data = {
                    'success': False,
                }
            else:
                try:
                    post = Post.objects.get(id = post_id)
                    reaction, created = Reaction.objects.update_or_create(post = post, reactor = request.user, defaults = {'reaction': int(reaction_number)})

                    data = {
                        'success': True,
                        'reactions': modify(post.postreactions.count()),
                        'plural': 's' if (post.postreactions.count() > 1) else '',
                    }
                except:
                    data = {
                        'success': False,
                    }

            return JsonResponse(data)
        else:
            return HttpResponseForbidden()


class CommentView(LoginRequiredMixin, View):
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            comment_text = request.POST.get('comment_text', None)
            post_id = request.POST.get('post_id', None)
            comment_image = request.FILES.get('comment_image', None)

            if (comment_text == None and comment_image == None) or post_id == None:
                data = {
                    'success': False,
                }
            else:
                try:
                    post = Post.objects.get(id = post_id)
                    new_comment = Comment(post = post, Commentor = request.user, comment_text = comment_text, comment_image = comment_image)
                    new_comment.save()

                    data = {
                        'success': True,
                        'new_comment_html': render_to_string('post/extra_comment.html', {'comment': new_comment,}),
                        'comments': modify(post.comments.count()),
                        'plural': 's' if (post.comments.count() > 1) else '',
                    }
                except:
                    if not new_comment == None:
                        new_comment.delete()
                    
                    data = {
                        'success': False,
                    }
            
            return JsonResponse(data)
        else:
            return HttpResponseForbidden()


class ExtraDataView(LoginRequiredMixin, View):
    http_method_names = ['get',]

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            what = request.GET.get('what', None)
            post_id = request.GET.get('post_id', None)
            loaded = request.GET.get('loaded', None)

            if what == None or loaded == None or post_id == None:
                data = {
                    'success': False,
                }
            else:
                if what == 'comment':
                    try:
                        loaded = int(loaded)
                        post = Post.objects.get(id = post_id)
                        extra_comments = Comment.objects.filter(post = post).order_by('-comment_created')[loaded : loaded + 3]

                        data = {
                            'success': True,
                            'total': Comment.objects.filter(post = post).count(),
                            'extra_comments': list(render_to_string('post/extra_comment.html', {'comment': comment,}) for comment in extra_comments),
                        }
                    except:
                        data = {
                            'success': False,
                        }
            
            return JsonResponse(data)
        else:
            return HttpResponseForbidden()


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post/new_post.html'

    def get_success_url(self):
        return reverse('postdetails', args = (self.object.id,))
    
    def get_initial(self):
        return {'owner': self.request.user,}

    def form_valid(self, form):
        images = self.request.FILES.getlist('post_images')

        if len(images) > 50:
            form.add_error(field = 'post_images', error = 'Cannot upload more than 50 images')
            return self.form_invalid(form)
        else:
            valid = super(CreatePostView, self).form_valid(form)
            post_obj = self.object

            if not images == []:
                for image in images:
                    PostImage.objects.create(post = post_obj, image = image)

            return valid


class NotificationView(LoginRequiredMixin, ListView):
    template_name = 'post/notification.html'

    def get_queryset(self):
        return self.request.user.notifications.all_unread()
    
    def get_context_data(self, **kwargs):
        context = super(NotificationView, self).get_context_data(**kwargs)
        context['notif_no'] = self.request.user.notifications.all_unread().count()
        return context
'''