from django.apps import AppConfig


class StoresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "features.stores"
    verbose_name = "Lojas"
    divider_title = "Lojas"
    icon = "fa fa-solid fa-store"


# <i class="fa-solid fa-store"></i>
