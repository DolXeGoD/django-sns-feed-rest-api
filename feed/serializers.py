from .models import Feed,Like,Comment
from rest_framework import serializers

class FeedDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('feed_md_image', 'feed_md_name', 'feed_content', 'feed_upload_dttm')

class FeedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('feed_md_image', 'feed_md_name', 'feed_content', 'feed_upload_dttm')

class FeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('feed_md_image', 'feed_md_name', 'feed_content')

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('feed_id', 'user_id', 'comment', 'upload_dttm', 'update_dttm')

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('feed_id', 'user_id', 'comment')

class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user_id', 'comment')

class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user_id',)