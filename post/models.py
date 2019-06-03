from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from shareland.commons import get_path

# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Owner')
    heading = models.CharField('Post heading', max_length = 100, default = '')
    post_text = models.TextField('Post text', default = '')
    creation_date = models.DateTimeField('Creation date & time', default = localtime)

    def __str__(self):
        head = str(self.heading)
        trailing = '...' if len(head) > 8 else ''
        return (head[:8].strip() + trailing)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'ImagePost')
    image = models.ImageField('Image', upload_to = get_path)

    class Meta:
        verbose_name = 'Post related image'
        verbose_name_plural = 'Post related images'


class Reaction(models.Model):
    REACTIONS = [
        (1, 'Likeit'),
        (2, 'Facepalm'),
        (3, 'Lovely'),
        (4, 'Laughing'),
        (5, 'Spellbound'),
        (6, 'Sad'),
        (7, 'Raging'), 
    ]

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'ReactionPost')
    reactor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Reactor', null = True)
    reaction = models.PositiveSmallIntegerField('Reaction', choices = REACTIONS)

    class Meta:
        verbose_name = 'Reaction'
        verbose_name_plural = 'Reactions'
    
    def clean(self):
        if Reaction.objects.filter(reactor__exact = self.reactor):
            raise ValidationError('One user one reactions')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'CommentPost')
    Commentor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Commentor', null = True)
    comment_text = models.TextField('Textual comment', blank = True, null = True)
    comment_image = models.ImageField('Image comment', upload_to = get_path, blank = True, null = True)

    def clean(self):
        if self.comment_text == None and self.comment_image == None:
            raise ValidationError('No comment given')


@receiver(post_delete, sender = PostImage)
def delete_image(sender, instance, **kwargs):
    instance.image.delete(False)
    return

@receiver(post_delete, sender = Comment)
def delete_image(sender, instance, **kwargs):
    instance.comment_image.delete(False)
    return