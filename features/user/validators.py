from django.core.exceptions import ValidationError

from features.user.models import TypeUser, User


def validate_logistic(pk):
    user = User.objects.get(pk=pk)

    if user.type_user != TypeUser.LOGISTIC:
        raise ValidationError(
            "Apenas usuários do tipo 'logistas' são aceitos neste campo"
        )

    return pk
