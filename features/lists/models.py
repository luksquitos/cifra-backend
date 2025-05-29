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
        products_list = self.products.all()
        if not products_list.exists():
            self.best_store = None
            self.total_price = None
            self.last_update = None
            self.save()
            return

        product_list_name = self.products.all().values_list("name", flat=True)

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
            self.best_store = None
            self.total_price = None
            self.last_update = None
            self.save()
            return

        # Sort by lower price.
        products_grouped.sort(key=lambda store_tuple: store_tuple[-1])
        best_spot = products_grouped[0]

        # Update UserList best spot values
        store_pk, queryset, total_price = best_spot
        self.best_store = Store.objects.get(pk=store_pk)
        self.total_price = total_price
        self.last_update = datetime.now()
        self.save()

        # TODO Update products price, and total_price

    class Meta:
        verbose_name = "Lista de Usuário"
        verbose_name_plural = "Listas de Usuários"


class ProductList(models.Model):
    user_list = models.ForeignKey(
        "lists.UserList", models.CASCADE, related_name="products", verbose_name="Lista"
    )
    name = models.CharField("Nome", max_length=200)
    quantity = models.PositiveSmallIntegerField("Quantidade de itens")
