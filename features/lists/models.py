from django.db import models


class UserList(models.Model):
    user = models.ForeignKey(
        "user.User", models.CASCADE, related_name="lists", verbose_name="Usuário"
    )
    name = models.CharField("Nome", max_length=64)
    # Best purchase spot
    total_price = models.DecimalField(
        verbose_name="Preço total",
        max_digits=12,
        decimal_places=2,
        help_text="Valor total dos produtos do melhor local de compra",
        null=True,
        blank=True,
    )
    better_store = models.ForeignKey(
        "stores.Store",
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Melhor Loja",
    )
    last_update = models.DateTimeField("Última atualização", null=True, blank=True)

    def calculate_best_spot(self):
        # Caminhos para encontrar o melhor preço
        # - Encontrar as lojas que tem os produtos mencionados junto com sua quantidade
        # - A soma dos produtos deve ser a menor.
        pass

    class Meta:
        verbose_name = "Lista de Usuário"
        verbose_name_plural = "Listas de Usuários"


class ProductList(models.Model):
    user_list = models.ForeignKey(
        "lists.UserList", models.CASCADE, related_name="products", verbose_name="Lista"
    )
    name = models.CharField("Nome", max_length=200)
    quantity = models.PositiveSmallIntegerField("Quantidade de itens")
