from rest_framework import serializers
from django.contrib.auth.models import User
from notifications.models import *
from .models import *

# Serializer classes are here

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ('id', 'image',)


class PostSerializer(serializers.ModelSerializer):

    postimages = PostImageSerializer(many = True)
    total_reactions = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    owner_full_name = serializers.SerializerMethodField()
    owner_avatar = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'heading', 'post_text', 'creation_date', 'postimages', 'total_reactions', 'total_comments', 'owner_full_name', 'owner_avatar','owner_id',)
        extra_kwargs = {
            'creation_date': {'read_only': True, 'required': False,},
        }
    
    def get_total_reactions(self, obj):
        return obj.postreactions.count()
    
    def get_total_comments(self, obj):
        return obj.comments.count()
    
    def get_owner_full_name(self, obj):
        return obj.owner.get_full_name()
    
    def get_owner_avatar(self, obj):
        return self.context.get('request').build_absolute_uri(obj.owner.userprofile.avatar.url)
    
    def get_owner_id(self, obj):
        return obj.owner.id
    
    def create(self, validated_data):
        postimage_data = validated_data.pop('postimages')

        post = self.Meta.model.objects.create(owner = self.context['request'].user, **validated_data)

        for postimage in postimage_data:
            PostImage.objects.create(post = post, **postimage)

        return post
    
    def update(self, instance, validated_data):
        postimages = validated_data.pop('postimages')
        postimages_count = len(postimages)

        instance.heading = validated_data.get('heading', instance.heading)
        instance.post_text = validated_data.get('post_text', instance.post_text)
        instance.save()

        post_images = instance.postimages
        post_images_count = len(post_images)

        # Equal no. of images come from update form, so update them all
        if postimages_count == post_images_count:
            for i in range(postimages_count):
                post_images[i].image = postimages[i].get('image', post_images[i].image)
                post_images[i].save()
        # More no. of images come from update form, so update and create some images
        elif postimages_count > post_images_count:
            for i in range(post_images_count):
                post_images[i].image = postimages[i].get('image', post_images[i].image)
                post_images[i].save()
            for image in postimages[post_images_count:]:
                postimage = PostImage.objects.create(post = instance, **image)
        # Less no. of images come from update form, so update and delete extra images
        else:
            for i in range(postimages_count):
                post_images[i].image = postimages[i].get('image', post_images[i].image)
                post_images[i].save()
            for image in post_images[postimages_count:]:
                image.delete()
        
        return instance


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'reaction',)
    
    def update(self, instance, validated_data):
        instance.reaction = validated_data.get('reaction', instance.reaction)
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):

    total_replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'comment_image', 'comment_created', 'replies', 'total_replies',)

    def get_total_replies(self, obj):
        return obj.replies.count()
    
    def update(self, instance, validated_data):
        instnace.comment_text = validated_data.get('comment_text', instance.comment_text)
        instance.comment_image = validated_data.get('comment_image', instance.comment_image)
        instance.save()

        return instance

CommentSerializer._declared_fields['replies'] = CommentSerializer(many = True)


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id', 'source_display_name', 'action', 'category', 'obj', 'url', 'short_description', 'extra_data', 'update_date',)




