from rest_framework import serializers
from notifications.models import *
from .models import *

# Serializer classes are here

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ('id', 'image',)
    
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance   


class PostSerializer(serializers.ModelSerializer):

    postimages = PostImageSerializer(many = True)

    class Meta:
        model = Post
        fields = ('id', 'heading', 'post_text', 'creation_date', 'postimages',)
    
    def create(self, validated_data):
        postimage_data = validated_data.pop('postimages')

        post = super(PostImageSerializer, self).create(validated_data)

        for postimage in postimages:
            Postimage.object.create(post = post, **postimage)

        return post


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'reaction',)
    
    def update(self, instance, validated_data):
        instance.reaction = validated_data.get('reaction', instance.reaction)
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'comment_image', 'comment_created', 'replies',)
    
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
