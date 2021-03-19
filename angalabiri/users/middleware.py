from django.contrib.auth.models import AnonymousUser
from .models import User

class UserIPAccessMiddleware(object):
    """
        Save the Ip address if does not exist
    """
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META["HTTP_USER_AGENT"]

        try:
            User.objects.get(ip_address=ip, accessed_with=user_agent)

        except User.DoesNotExist:             #-----Here My Edit
            user = User(ip_address=ip)
            user = User(accessed_with=user_agent)
            user.save()
        return None
