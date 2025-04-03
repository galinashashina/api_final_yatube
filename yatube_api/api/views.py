from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    def get_post(self):
        """Вспомогательный метод для получения поста по id."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает комментарии к конкретному посту."""
        return Comment.objects.filter(post=self.get_post())

    def perform_create(self, serializer):
        """Добавляет комментарий к конкретному посту."""
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        following_username = self.request.data.get("following")
        if Follow.objects.filter(
            user=self.request.user,
            following__username=following_username
        ).exists():
            raise ValidationError("Вы уже подписаны на этого пользователя.")
        serializer.save(user=self.request.user)
# Тут возникли серьёзные сложности - постоянно ошибка в тестах -
# AssertionError: Проверьте, что POST-запрос с корректными данными,
# отправленный к /api/v1/follow/, возвращает ответ со статусом 201. -
# поэтому оставила без изменений.


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
