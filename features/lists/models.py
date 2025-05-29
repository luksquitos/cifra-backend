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
        """Finds the cheapest store that contains all products from the user's list
        with the desired quantities."""

        products_in_list = self.products.all()
        if not products_in_list:
            return  # Empty list

        # 1. Get the desired product names and quantities from the list
        desired_products_map = {p.name: p.quantity for p in products_in_list}
        desired_product_names = list(desired_products_map.keys())

        # 2. Find all candidate stores that have ALL products from the list
        # and with sufficient quantity.
        # We'll use a product count approach to ensure all are present.

        candidate_store_ids = []

        # First, identify stores that have *all* the products from the list,
        # regardless of quantity initially.
        # We use GroupBy and Count to ensure the number of products found
        # in the store is equal to the number of products in the list.
        stores_with_all_products = (
            Store.objects.filter(  # TODO Adicionar Prefetch Related
                products__name__in=desired_product_names
            )
            .annotate(num_products_found=models.Count("products__name", distinct=True))
            .filter(num_products_found=len(desired_product_names))  # gte
            .values_list("id", flat=True)
        )

        qualified_stores = []
        min_total_price = float("inf")
        best_store = None

        for store_id in stores_with_all_products:
            store_obj = Store.objects.get(id=store_id)
            current_store_total_price = 0
            store_meets_criteria = True

            for desired_product_name, desired_quantity in desired_products_map.items():
                try:
                    product_in_store = Product.objects.get(
                        store=store_obj, name=desired_product_name
                    )
                    if product_in_store.quantity >= desired_quantity:
                        current_store_total_price += (
                            product_in_store.price * desired_quantity
                        )
                    else:
                        store_meets_criteria = False
                        break  # The store doesn't have enough quantity for this product
                except Product.DoesNotExist:
                    store_meets_criteria = False
                    break  # The product doesn't exist in this store (though the first phase should filter this out)

            if store_meets_criteria:
                if current_store_total_price < min_total_price:
                    min_total_price = current_store_total_price
                    best_store = store_obj

        # Update the UserList if a store is found
        if best_store:
            my_user_list.best_spot = best_store
            my_user_list.total_price = min_total_price
            my_user_list.save()
            return best_store, min_total_price
        else:
            # If no store is found, reset the list fields
            my_user_list.best_spot = None
            my_user_list.total_price = 0.00
            my_user_list.save()
            return None, 0.00

    class Meta:
        verbose_name = "Lista de Usuário"
        verbose_name_plural = "Listas de Usuários"


class ProductList(models.Model):
    user_list = models.ForeignKey(
        "lists.UserList", models.CASCADE, related_name="products", verbose_name="Lista"
    )
    name = models.CharField("Nome", max_length=200)
    quantity = models.PositiveSmallIntegerField("Quantidade de itens")


"""json
{
    Cimento 20kg: [1, 4, 5],
    "Pá de Coveiro": [1],
    "Soda Caustica": [2]
}

ProductList.objects.all()
# Loja
{
    2: {}
}
options = [
    {2: 4400},
    {5: 4300}
]
"""

# Sugestion to try.

"""python

products = Product.objects.filter(name__in=product_list_name)
.annotate(
    wished_quantity=Subquery(
        ProductList.objects.filter(
            name=OuterRef("name"),
            user_list=self
        )
        .values("quantity")
        [:1]
    )
)
.filter(quantity__gte(F("wished_quantity")))

stores = products.values_list("store__pk", flat=True)

products_grouped = []

# Group by store
for store_pk in stores:
    products_grouped.append(
        {store_pk: products.filter(store__pk=store_pk)}
    )

"""
