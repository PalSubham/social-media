from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy
from shareland.commons import show_pic, LinkToInlineObject

# Register your models here.

admin.site.site_header = gettext_lazy('sharELand administration')
admin.site.site_title = gettext_lazy('sharELand site admin')
admin.site.index_title = gettext_lazy('sharELand admin panel')

show_pic.short_description = gettext_lazy('Image')

class PostImageInline(admin.StackedInline):
    model = PostImage
    fields = ('image', show_pic,)
    readonly_fields = (show_pic,)
    extra = 0


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
