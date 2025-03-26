from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from features.user.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"username": "email"}


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "is_staff",
            "date_joined",
            "password",
            "last_login",
            "is_superuser",
            "groups",
            "user_permissions",
        ]
        field_classes = {"username": "email"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )
