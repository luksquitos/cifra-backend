from decimal import Decimal
from re import sub

from django.core.validators import MinValueValidator
from django.db import models

# from django.dispatch import receiver


class Store(models.Model):
    name = models.CharField("Nome", max_length=200)

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
    name = models.CharField("Nome", max_length=200)
    about = models.TextField("Sobre", help_text="Sobre o produto")
    category = models.ForeignKey(
        "stores.Category", models.CASCADE, verbose_name="Categoria"
    )
    price = models.DecimalField(
        verbose_name="Preço",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    image = models.ImageField("Imagem", upload_to=product_directory_path, null=True)

    def __str__(self):
        return f"{self.name} R${self.price}"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["price"]


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
    created_at = (
        models.DateTimeField()
    )  # FIXME Depois de criar os dados falsos, isso precisa ser auto_now_add=True

    class Meta:
        verbose_name = "Histórico de preço de produto"
        verbose_name_plural = "Históricos de preço de produto"
        ordering = ["price"]


# @receiver(models.signals.post_save, sender=Product)
# def create_price_product_history(sender, instance, created, **kwargs):
#     if created:
#         print("Criado ", instance, kwargs.get("update_fields"))
#         # PriceProductHistory.objects.create(
#         #     product=instance,
#         #     price=instance.price
#         # )
#     print("update_fields ", kwargs.get("update_fields"))
