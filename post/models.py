from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError
from shareland.commons import get_path

# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    heading = models.CharField('Post heading', max_length = 100, default = '')
    post_text = models.TextField('Post text', blank = True, null = True)
    creation_date = models.DateTimeField('Creation date & time', default = localtime)

    def __str__(self):
        head = str(self.heading)
        trailing = '...' if len(head) > 8 else ''
        return (head[:8].strip() + trailing)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'postimages')
    image = models.ImageField('Image', upload_to = get_path)

    class Meta:
        verbose_name = 'Post related image'
        verbose_name_plural = 'Post related images'
    
    def __str__(self):
        return 'Image for {0}, id = {1}'.format(str(self.post), str(self.pk))


class Reaction(models.Model):
    REACTIONS = [
        (1, 'ok-hand'),
        (2, 'expressionless-face'),
        (3, 'sparkling-heart'),
        (4, 'rolling-on-floor-laughing'),
        (5, 'face-with-open-mouth'),
        (6, 'crying-face'),
        (7, 'pouting-face'), 
    ]

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'postreactions')
    reactor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'reactor')
    reaction = models.PositiveSmallIntegerField('Reaction', choices = REACTIONS)

    class Meta:
        verbose_name = 'Reaction'
        verbose_name_plural = 'Reactions'
    
    def clean(self):
        if not self.pk and Reaction.objects.filter(reactor__exact = self.reactor):
            raise ValidationError('One user one reactions')
    
    def __str__(self):
        return 'Reaction on {0} by {1}, id = {2}'.format(str(self.post), str(self.reactor), str(self.pk))


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments', blank = True, null = True)
    Commentor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Commentor')
    comment_text = models.TextField('Textual comment', blank = True, null = True)
    comment_image = models.ImageField('Image comment', upload_to = get_path, blank = True, null = True)
    comment_created = models.DateTimeField('Commented at', default = localtime)
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'replies', on_delete = models.CASCADE)

    class Meta:
        ordering = ['comment_created',]

    def clean(self):
        if not self.comment_text and not self.comment_image:
            raise ValidationError('No comment given')
    
    def __str__(self):
        if not self.parent:
            return 'Comment on {0} by {1}, id = {2}'.format(str(self.post), str(self.Commentor), str(self.pk))
        else:
            return 'Reply to comment id = {0} on {1} by {2}, id = {3}'.format(str(self.parent.pk), str(self.post), str(self.Commentor), str(self.pk))



@receiver(post_delete, sender = PostImage)
def delete_image(sender, instance, **kwargs):
    instance.image.delete(False)
    return

@receiver(post_delete, sender = Comment)
def delete_image(sender, instance, **kwargs):
    instance.comment_image.delete(False)
    return