from django.db import models
from django.db.models import F, OuterRef, Subquery, Sum
from django.utils.timezone import datetime

from features.stores.models import Product, Store


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
    best_store = models.ForeignKey(
        "stores.Store",
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Melhor Loja",
    )
    last_update = models.DateTimeField("Última atualização", null=True, blank=True)

    def calculate_best_spot(self):
        """Finds the cheapest store that contains all products from the user's list
        with the desired quantities."""

        self.products_list = self.products.all()
        if not self.products_list.exists():
            self._reset_best_spot_info()
            return

        product_list_name = self.products_list.values_list("name", flat=True)

        products = (
            Product.objects.filter(name__in=product_list_name)
            .annotate(
                wished_quantity=Subquery(
                    ProductList.objects.filter(
                        name=OuterRef("name"), user_list=self
                    ).values("quantity")[:1]
                )
            )
            .filter(quantity__gte=F("wished_quantity"))
            .annotate(total_price=F("wished_quantity") * F("price"))
        )

        stores = set(products.values_list("store__pk", flat=True))

        products_grouped = []
        products_list_count = len(product_list_name)  #

        # Group by store
        for store_pk in stores:
            store_products_available = products.filter(store__pk=store_pk)

            if products_list_count != store_products_available.count():
                continue  # Store doesn't have all list items

            products_grouped.append(
                (
                    store_pk,
                    store_products_available,
                    store_products_available.aggregate(total=Sum("total_price"))[
                        "total"
                    ],
                )
            )

        if not products_grouped:  # Any stores has wished items.
            self._reset_best_spot_info()
            return

        # Sort by lower price.
        products_grouped.sort(key=lambda store_tuple: store_tuple[-1])
        best_spot = products_grouped[0]

        # Update UserList best spot values
        self._update_list_values(best_spot)

    def _update_list_values(self, best_spot: tuple):
        store_pk, queryset, total_price = best_spot
        self.best_store = Store.objects.get(pk=store_pk)
        self.total_price = total_price
        self.last_update = datetime.now()
        self.save()
        queryset_map = {p.name: p for p in queryset}

        for product in self.products.all():
            store_product = queryset_map.get(product.name)
            product.price = store_product.price
            product.total_price = store_product.total_price
            if not product.image:
                product.image = store_product.image

            product.save()

    def _reset_best_spot_info(self):
        self.best_store = None
        self.total_price = None
        self.last_update = None
        self.save()

        if not self.products_list.exists():
            return

        for product in self.products_list:
            product.price = None
            product.total_price = None

        ProductList.objects.bulk_update(self.products_list, ["price", "total_price"])

    def __str__(self):
        return f"Lista de {self.name}"

    class Meta:
        verbose_name = "Lista de Usuário"
        verbose_name_plural = "Listas de Usuários"


def product_directory_path(instance, filename):
    return (
        f"lists/{instance.user_list.user.email}/{instance.user_list.pk}/{instance.name}"
    )


class ProductList(models.Model):
    user_list = models.ForeignKey(
        "lists.UserList", models.CASCADE, related_name="products", verbose_name="Lista"
    )
    name = models.CharField("Nome", max_length=200)
    quantity = models.PositiveSmallIntegerField("Quantidade de itens")
    price = models.DecimalField(
        verbose_name="Preço",
        max_digits=12,
        decimal_places=2,
        help_text="Valor do produto no melhor local de compra",
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        verbose_name="Preço total",
        max_digits=12,
        decimal_places=2,
        help_text="Valor total dos produtos do melhor local de compra baseado na quantidade",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        "Imagem", upload_to=product_directory_path, null=True, blank=True
    )
