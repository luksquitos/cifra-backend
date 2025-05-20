from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth.forms import BaseUserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from features.stores.models import Store
from features.user.models import TypeUser, User


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


class LogisticSignUpForm(forms.ModelForm):
    # Campos do usuário
    name = forms.CharField(label="Nome", widget=AdminTextInputWidget)
    email = forms.EmailField(label="Email", widget=AdminTextInputWidget)
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    # Campos da loja
    store_name = forms.CharField(label="Nome da Loja", widget=AdminTextInputWidget)
    store_address = forms.CharField(label="Endereço", widget=AdminTextInputWidget)
    store_cnpj = forms.CharField(label="CNPJ", widget=AdminTextInputWidget)

    class Meta:
        model = User
        fields = ("name", "email")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = User(
            name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            type_user=TypeUser.LOGISTIC,
            is_staff=True,
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

            # Add logistic to logistics group
            group = Group.objects.get(name="logistics")
            user.groups.add(group)

            # Create store
            Store.objects.create(
                user=user,
                name=self.cleaned_data["store_name"],
                address=self.cleaned_data["store_address"],
                cnpj=self.cleaned_data["store_cnpj"],
            )
        return user
