from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuper(BasePermission):
    message = 'Доступ разрешен только администратору'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_or_super


class IsAdminOrReadOnly(BasePermission):
    message = 'Доступ разрешен только администратору'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin_or_super
        )


class IsStaffOrAuthorOrReadOnly(BasePermission):
    message = 'Доступ разрешен только администратору, модератору или автору'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin_or_super
            or request.user.is_moderator
            or request.user == obj.author
        )
