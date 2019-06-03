from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy
from shareland.commons import show_pic, LinkToInlineObject

# Register your models here.

show_pic.short_description = gettext_lazy('Image')

class PostImageInline(admin.StackedInline):
    model = PostImage
    fields = ('image', show_pic,)
    readonly_fields = (show_pic,)
    extra = 0


class ReactionInline(admin.StackedInline):
    model = Reaction
    fields = ('reactor', 'reaction',) 
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ReactionInline,]
    readonly_fields = ('creation_date',)

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }
