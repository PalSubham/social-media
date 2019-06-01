from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.

admin.site.unregister(User)

# Shows avatar in admin panel. Actually returns its url
@mark_safe
def show_avatar(obj):
    return """<img src="{src}" alt="Avatar" style="max-width: 200px; max-height: 200px;"/>""".format(src = obj.avatar.url)

show_avatar.short_description = gettext_lazy('Avatar')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('timezone', 'follows', 'avatar', show_avatar)
    readonly_fields = (show_avatar,)
    filter_horizontal = ('follows',)

class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline,]

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }

admin.site.register(User, MyUserAdmin)
