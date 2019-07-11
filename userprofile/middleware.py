from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
import pytz
from .models import *


# Activates timezone for a logged in user
class ActivateTimezoneMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            tzname = UserProfile.objects.get(owner = request.user).timezone

            if tzname:
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
        else:
            timezone.deactivate()
        
        return