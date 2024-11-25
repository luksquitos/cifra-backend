from django.db import models


class Product(models.Model):
    construtor = models.CharField("Construtora", max_length=200)
    name = models.CharField("Nome do Produto", max_length=500)
    price = models.FloatField("Preço do produto")
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"