from django.contrib import admin
from .models import *
from notifications.models import *
from django.utils.translation import gettext_lazy
from shareland.commons import show_pic, LinkToInlineObject

# Register your models here.

admin.site.site_header = gettext_lazy('sharELand administration')
admin.site.site_title = gettext_lazy('sharELand site admin')
admin.site.index_title = gettext_lazy('sharELand admin panel')

admin.site.unregister(Notification)

show_pic.short_description = gettext_lazy('Image')

class PostImageInline(admin.StackedInline):
    model = PostImage
    fields = ('image', show_pic,)
    readonly_fields = (show_pic,)
    extra = 0
    max_num = 50


class ReactionInline(admin.StackedInline):
    model = Reaction
    fields = ('reactor', 'reaction',)
    radio_fields = {'reaction': admin.HORIZONTAL,}
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ReactionInline, CommentInline,]

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('create_date', 'update_date',)

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }