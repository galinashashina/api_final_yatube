from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = fields = ['id', 'author', 'post', 'text', 'created']
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписок."""

    user = serializers.StringRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ['id', 'user', 'following']

    def validate_following(self, value):
        """Запрещает подписываться на самого себя."""
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return value

    def create(self, validated_data):
        """Создаёт подписку с username."""
        user = self.context['request'].user
        following_user = validated_data.get('following')
        follow = Follow.objects.create(user=user, following=following_user)
        return follow


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']
