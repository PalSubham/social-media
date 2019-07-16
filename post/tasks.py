from celery.decorators import task
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.auth.models import User

@task(name = 'notif')
def notif(poster_id, post_id, post_detail):
    poster = User.objects.get(id = poster_id)

    for follower in poster.userprofile.get_followers():
        notif_args = {
            'source': poster,
            'source_display_name': poster.get_full_name(),
            'recipient': follower.owner,
            'category': 'post',
            'action': 'shared',
            'obj': post_id,
            'url': post_detail,
            'short_description': 'a new post.',
        }

        notify.send(sender = notif, **notif_args, channels = ['websocket',])

    return

@task(name = 'del_notif_task')
def del_notif_task(post_id):
    for notif in Notification.objects.filter(obj = post_id):
        notif.delete()
    
    return