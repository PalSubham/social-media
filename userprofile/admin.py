from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from .models import *
from post.models import Post
from shareland.commons import show_pic, LinkToInlineObject

# Register your models here.

admin.site.unregister(User)

show_pic.short_description = gettext_lazy('Avatar')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('birthday', 'timezone', 'follows', 'avatar', show_pic,)
    readonly_fields = (show_pic,)
    filter_horizontal = ('follows',)


class PostInline(admin.StackedInline, LinkToInlineObject):
    model = Post
    readonly_fields = ('creation_date', 'get_link',)
    extra = 0


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline, PostInline,]

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }
