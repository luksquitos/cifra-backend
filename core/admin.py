from admin_interface.admin import ThemeAdmin
from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth.models import Group


class AdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)  #

        if request.user.is_superuser:
            return app_list

        to_remove = ["PriceProductHistory", "Store", "ProductTechnicalCharacteristics"]

        for app in app_list:
            if app["app_label"] != "stores":
                continue

            original = app["models"]
            app["models"] = [m for m in original if m["object_name"] not in to_remove]

        return app_list


site = AdminSite("admin")


@admin.register(Theme, site=site)
class ThemeAdmin(ThemeAdmin):
    pass


@admin.register(Group, site=site)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ["permissions"]
