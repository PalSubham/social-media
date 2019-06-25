from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

# Here are the mixins

class EnsureCSRFCookieMixin(object):
    '''
    Ensures that CSRF cookie will be passed to the client.
    This should be the left most mixin of a view
    '''

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(EnsureCSRFCookieMixin, self).dispatch(*args, **kwargs)