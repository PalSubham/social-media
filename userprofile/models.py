from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shareland.commons import get_path
import pytz

# Create your models here.

class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE)
    follows = models.ManyToManyField('self', related_name = 'followed_by', symmetrical = False, blank = True)
    timezone = models.CharField("User's timezone", max_length = 20, default = 'UTC')
    avatar = models.ImageField("Change avatar", upload_to = get_path, default = 'default_avatar.png')
    birthday = models.DateField('Birthday', null = True)

    class Meta:
        verbose_name = 'Profile data'
        verbose_name_plural = 'Profile data'
    
    def __str__(self):
        return str(self.owner)


# This will create a UserProfile object for a new User
@receiver(post_save, sender = User)
def create_UserProfile_object(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(owner = instance)
    return


@receiver(post_delete, sender = UserProfile)
def delete_image(sender, instance, **kwargs):
    instance.avatar.delete(False)
    return
