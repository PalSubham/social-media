# Here stays the common classes and functions, used by the apps

from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy

# To get a sense of nested inline object
class LinkToInlineObject(object):
    def get_link(self, instance):
        url = reverse('admin:{0}_{1}_change'.format(instance._meta.app_label, instance._meta.model_name), args = [instance.pk,])
        if instance.pk:
            return mark_safe(u'<a href="{0}">Get details</a>'.format(url))
        else:
            return ''
    
    get_link.short_description = gettext_lazy('Link to details')


# Shows avatar in admin panel. Actually returns its url
@mark_safe
def show_pic(obj):
    try:
        src = obj.image.url
    except:
        src = obj.avatar.url
    
    return """<img src="{0}" alt="Avatar" style="max-width: 200px; max-height: 200px;"/>""".format(src)


# Creates directory for each user to store their posted images and avatar
def get_path(instance, filename):
    try:
        which_pk = instance.owner.pk
    except:
        which_pk = instance.post.owner.pk
    
    return 'user_{0}/{1}'.format(which_pk, filename)