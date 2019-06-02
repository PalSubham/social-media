from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from django.core.exceptions import ValidationError

# Create your models here.

# Creates directory for each user to store their avatar
def get_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.post.owner.pk, filename)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Owner')
    heading = models.CharField('Post heading', max_length = 100, default = '')
    post_text = models.TextField('Post text', default = '')
    creation_date = models.DateTimeField('Creation date & time', blank = True, null =True)
    edited = models.DateTimeField('Edited at', blank = True, null = True)

    def __str__(self):
        head = str(self.heading)
        trailing = '...' if len(head) > 8 else ''
        return (head[:8].strip() + trailing)

    def save(self, *args, **kwargs):
        if not self.pk == None:
            self.edited = localtime()
        
        return super(Post, self).save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'Post')
    image = models.ImageField('Image', upload_to = get_path)
    created = models.DateTimeField('Created at', blank = True, null = True)

    class Meta:
        verbose_name = 'Post related image'
        verbose_name_plural = 'Post related images'

    def save(self, *args, **kwargs):
        if self.pk == None:
        	self.created = localtime()
        
        return super(PostImage, self).save(*args, **kwargs)


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

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'Post image+')
    reactor = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Reactor')
    reaction = models.PositiveSmallIntegerField('Reaction', choices = REACTIONS)

    class Meta:
        verbose_name = 'Reaction'
        verbose_name_plural = 'Reactions'
    
    def clean(self):
        if Reaction.objects.filter(reactor__exact = self.reactor):
            raise ValidationError('One user one reactions')
        
        