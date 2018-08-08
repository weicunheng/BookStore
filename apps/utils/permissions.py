from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级别的权限
    只允许对象的所有者编辑
    假设模型实例具有"所有者"属性
    """

    def has_object_permission(self, request, view, obj):
        # 允许任何读权限
        # 所以允许 GET, HEAD or OPTIONS 请求.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 其他权限比如post  delete 需要实例必须有一个"所有者"属性
        return obj.user == request.user
