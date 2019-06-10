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


class UserProfileInline(admin.StackedInline, LinkToInlineObject):
    model = UserProfile
    fields = ('birthday', 'timezone', 'avatar', show_pic, 'get_link',)
    readonly_fields = (show_pic, 'get_link',)


class PostInline(admin.StackedInline, LinkToInlineObject):
    model = Post
    readonly_fields = ('creation_date', 'get_link',)
    extra = 0


class RelationshipInline(admin.StackedInline):
    model = Relationship
    fk_name = 'from_person'
    radio_fields = {'status': admin.HORIZONTAL,}
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline,]

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }


@admin.register(User)
class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline, PostInline,]

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }
