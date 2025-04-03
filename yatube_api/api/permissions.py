from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Управление доступами.

    Разрешает редактирование и удаление только автору поста.
    Остальным пользователям доступно только чтение.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
