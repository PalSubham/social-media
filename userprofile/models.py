from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shareland.commons import get_path
import pytz

# Create your models here.

class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'userprofile')
    follows = models.ManyToManyField('self', related_name = 'followed_by', through = 'Relationship', symmetrical = False, blank = True)
    timezone = models.CharField("User's timezone", max_length = 20, default = 'UTC')
    avatar = models.ImageField("Change avatar", upload_to = get_path, default = 'default_avatar.png')
    birthday = models.DateField('Birthday', null = True)

    class Meta:
        verbose_name = 'Profile data'
        verbose_name_plural = 'Profile data'
    
    def __str__(self):
        return 'For ' + str(self.owner)
    
    def add_following(self, person):
        return Relationship.object.get_or_create(from_person = self, to_person = person, status = 1)
    
    def remove_following(self, person):
        Relationship.objects.filter(from_person = self, to_person = person).delete()
        return
    
    def get_following(self):
        return self.follows.filter(to_people__from_person = self, to_people__status = 1)
    
    def get_followers(self):
        return self.followed_by.filter(from_people__to_person = self, from_people__status = 1)

    def get_blocked_followers(self):
        return self.followed_by.filter(from_people__to_person = self, from_people__status = 2)


class Relationship(models.Model):
    STATUSES = (
        (1, 'Following'),
        (2, 'Blocked'),
    )

    from_person = models.ForeignKey(UserProfile, related_name = 'from_people', on_delete = models.CASCADE)
    to_person = models.ForeignKey(UserProfile, related_name = 'to_people', on_delete = models.CASCADE)
    status = models.PositiveSmallIntegerField('Relationship status', choices = STATUSES)

    class Meta:
        verbose_name = 'Following'
        verbose_name_plural = 'Following'


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
