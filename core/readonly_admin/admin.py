from django.http.request import HttpRequest


class ReadonlyAdminMixin:
    def has_change_permission(self, request: HttpRequest, obj=None):
        if not obj:
            return super().has_change_permission(request, obj)

        if request.GET.get("view", "0") != "1":
            return super().has_change_permission(request, obj)

        return False
