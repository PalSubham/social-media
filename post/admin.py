from django.contrib import admin
from .models import *

# Register your models here.

class PostImageInline(admin.StackedInline):
    model = PostImage
    fields = ('image', 'created')
    readonly_fields = ('created',)
    extra = 0


class ReactionInline(admin.StackedInline):
    model = Reaction
    fields = ('reactor', 'reaction',)
    extra = 2


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ReactionInline,]
    readonly_fields = ('creation_date',)

    class Media:
        js = ('configadmin/js/no-tz-warning.js',)
        css = {
            'all': ('configadmin/css/no-tz-warning.css',)
        }

admin.site.register(Post, PostAdmin)
