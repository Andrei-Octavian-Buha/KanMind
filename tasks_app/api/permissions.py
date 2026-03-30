from rest_framework.permissions import BasePermission

class IsTaskCreatorOrBoardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.creator == request.user or
            obj.board.owner == request.user
        )