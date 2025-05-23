from decimal import Decimal
from re import sub

from django.core.validators import MinValueValidator
from django.db import models
from django.dispatch import receiver

from core.faker import fake
from core.validators import validate_cnpj
from features.user.validators import validate_logistic


class Store(models.Model):
    user = models.OneToOneField(
        "user.User",
        models.CASCADE,
        related_name="store",
        verbose_name="Lojista",
        validators=[validate_logistic],
        # TODO Remove after fixtures for all.
        null=True,
        blank=True,
    )
    name = models.CharField("Nome", max_length=200)
    address = models.CharField("Endereço", max_length=256, default=fake.address())
    cnpj = models.CharField(
        "CNPJ", max_length=18, validators=[validate_cnpj], default=fake.cnpj()
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"


class Category(models.Model):
    name = models.CharField("Nome", max_length=200)
    svg = models.TextField("SVG", null=True, blank=True)

    def update_svg_attributes(self, **kwargs):
        if not self.svg:
            return

        # These shouldn't be send.
        kwargs.pop("fill", None)
        kwargs.pop("d", None)
        kwargs.pop("xmlns", None)

        # Override fill for <svg>
        if "fill_svg" in kwargs:
            self.svg = sub(
                pattern=r'(<svg[^>]*\s)fill="[^"]*"',
                repl=rf'\1fill="{kwargs["fill_svg"]}"',
                string=self.svg,
            )

        # Override fill for <path>
        if "fill_path" in kwargs:
            self.svg = sub(
                pattern=r'(<path[^>]*\s)fill="[^"]*"',
                repl=rf'\1fill="{kwargs["fill_path"]}"',
                string=self.svg,
            )

        for key, value in kwargs.items():
            if key in ["fill_svg", "fill_path"]:
                continue

            self.svg = sub(
                pattern=rf'({key})="[^"]*"', repl=rf'\1="{str(value)}"', string=self.svg
            )

        return

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


def product_directory_path(instance, filename):
    store = instance.store.name.lower().replace(" ", "-")
    category = instance.category.name.lower().replace(" ", "-")

    return f"{store}/{category}/{instance.name}-{filename}"


class Product(models.Model):
    store = models.ForeignKey(
        "stores.Store", models.CASCADE, related_name="products", verbose_name="Loja"
    )
    category = models.ForeignKey(
        "stores.Category", models.CASCADE, verbose_name="Categoria"
    )
    name = models.CharField("Nome", max_length=200)
    quantity = models.PositiveIntegerField("Quantidade disponível")
    price = models.DecimalField(
        verbose_name="Preço",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Unidade",
    )
    image = models.ImageField(
        "Imagem", upload_to=product_directory_path, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} R${self.price}"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["price"]


class ProductTechnicalCharacteristics(models.Model):
    product = models.ForeignKey(
        "stores.Product", models.CASCADE, related_name="characteristics"
    )
    key = models.CharField("Nome da Característica")
    value = models.CharField("Característica")

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = "Caracteristica Técnica do Produto"
        verbose_name_plural = "Caracteristicas Técnicas do Produto"


class PriceProductHistory(models.Model):
    product = models.ForeignKey(
        "stores.Product",
        on_delete=models.CASCADE,
        related_name="historic",
        verbose_name="Produto",
    )
    price = models.DecimalField(
        verbose_name="Preço",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "Histórico de preço de produto"
        verbose_name_plural = "Históricos de preço de produto"
        ordering = ["-created_at"]


@receiver(models.signals.post_save, sender=Product)
def create_price_product_history(sender, instance, created, **kwargs):
    value = instance.price

    if not created:
        last_history = (
            PriceProductHistory.objects.select_related("product")
            .filter(product=instance)
            .first()
        )

        if last_history.price == value:
            return

    PriceProductHistory.objects.create(product=instance, price=value)
