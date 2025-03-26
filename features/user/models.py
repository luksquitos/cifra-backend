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
        

class UserToken(models.Model):
    """
    :email_template_path: Is used by core.mailer.tasks.send_email
    to instaciate the EmailTemplate class and send the email.
    """

    user = models.ForeignKey("user.User", models.CASCADE)
    token = models.CharField("Token", max_length=6)
    created_at = models.DateTimeField("Data de criação", auto_now_add=True)
    email_template_path = None

    def save(self, *args, **kwargs):
        self.token = self.generate_token()
        self.send_email()

        super().save(*args, **kwargs)

    def send_email(self):
        from core.mailer import send_email

        email_template_path = self.get_email_template_path()

        send_email.apply_async(
            countdown=2,
            args=[email_template_path],
            kwargs={
                "body_context": {"token": self.token},
                "to_emails": [self.user.email],
            },
        )

    def get_email_template_path(self) -> int:
        if self.email_template_path is None:
            raise ValueError("O template de email não foi fornecido")

        return self.email_template_path

    def generate_token(self):
        from random import randint

        return str(randint(100000, 999999))

    def is_valid(self):
        limit = self.created_at + timezone.timedelta(minutes=10)

        return limit > timezone.now()
        

class UserForgotPasswordToken(UserToken):
    email_template_path = None
