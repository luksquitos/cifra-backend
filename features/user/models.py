from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from core.faker import fake
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("E-mail", unique=True, blank=True)
    name = models.CharField("Nome", max_length=160)
    is_staff = models.BooleanField(
        "Membro da Equipe?",
        default=False,
        help_text="Indica que usuário consegue acessar este site de administração.",
    )
    date_joined = models.DateTimeField("Data de registro", default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @staticmethod
    def create_faker(data=None):
        data = data or {}

        if "password" in data:
            password = data.pop("password")
        else:
            password = None  

        data = {"email": fake.unique.email(), "name": fake.name(), **data}

        user = User.objects.create(**data)

        need_save = False

        if password:
            user.password = make_password(password)
            need_save = True

        if need_save:
            user.save()

        return user

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"