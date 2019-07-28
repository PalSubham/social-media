from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from knox.auth import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
import pytz

# Middlewares

# Activates timezone for a logged in user
class ActivateTimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        uri = request.build_absolute_uri()

        if 'admin' in uri and request.user.is_authenticated:
            user = request.user
        else:
            tokenauth = TokenAuthentication()

            try:
                user_token = tokenauth.authenticate(request)

                if user_token:
                    user = user_token[0]
                else:
                    timezone.deactivate()
                    return
            except AuthenticationFailed:
                timezone.deactivate()
                return
        
        tzname = user.userprofile.timezone

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

        return