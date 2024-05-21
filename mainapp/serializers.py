from autoslug import fields
from rest_framework import serializers

from .models import ArticleModel, Comments


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = [
            'article', 'text', 'author', 'created_at'
        ]


class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer

    class Meta:
        model = ArticleModel
        fields = [
            'name', 'slug', 'description', 'content',
            'is_published', 'time_created', 'time_updated',
            'author', 'photo', 'comments',
        ]
