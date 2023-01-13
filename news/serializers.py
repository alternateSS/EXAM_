from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from .models import News, Comment, NewsStatus, Status, CommentsStatus


class NewsSerializer(serializers.ModelSerializer):
    statuses = serializers.ReadOnlyField(source='get_status_count')

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['title', 'content']


class StatusNewsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(write_only=True)

    class Meta:
        model = NewsStatus
        fields = "__all__"
        read_only_fields = ['news', 'status', 'author']

    def create(self, validated_data):
        status_type = get_object_or_404(Status, slug=validated_data['slug'])
        validated_data.pop('slug')
        validated_data['type'] = status_type
        try:
            instance = super().create(validated_data)
        except IntegrityError:
            status_tweet = NewsStatus.objects.filter(**validated_data).first()
            if status_tweet:
                status_tweet.delete()
                raise serializers.ValidationError('У данной новости есть статус, текущий статус удален')
            else:
                status_type = validated_data.pop('type')
                status_tweet = NewsStatus.objects.get(**validated_data)
                status_tweet.type = status_type
                status_tweet.save()
                instance = status_tweet
        return instance


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author', 'news']