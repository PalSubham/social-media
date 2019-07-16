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
    total_reactions = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    owner_full_name = serializers.SerializerMethodField()
    owner_avatar = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'heading', 'post_text', 'creation_date', 'postimages', 'total_reactions', 'total_comments', 'owner_full_name', 'owner_avatar','owner_id',)
    
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




