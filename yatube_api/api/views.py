from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post
from .pagination import PostPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для публикаций."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        """Добавляет публикацию с автором, являющимся текущим пользователем."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Возвращает комментарии к конкретному посту."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Добавляет комментарий к конкретному посту."""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Обновляет комментарий, если он был создан текущим пользователем."""
        comment = self.get_object()
        if comment.author != self.request.user:
            return Response(
                {'detail': 'Вы не можете редактировать чужой комментарий.'},
                status=403
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Удаляет комментарий, если он был создан текущим пользователем."""
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужой комментарий.")
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления подписками."""

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """Возвращает подписки текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создает подписку от текущего пользователя."""
        following_user = self.request.data.get("following")
        if Follow.objects.filter(
            user=self.request.user,
            following__username=following_user
        ).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя.")
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
