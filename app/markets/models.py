from django.db import models

class Market(models.Model):
    # will have a owner ?
    name = models.CharField("Nome", max_length=100)
    endereco = models.CharField("Endereço", max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="products")
    name = models.CharField("Nome", max_length=100)
    price = models.DecimalField("Preço", decimal_places=2, max_digits=7)
    
    def __str__(self) -> str:
        return f"{self.name} R${self.price}"
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Imagem", upload_to="products-images") 
    #TODO Use a function to organize image folder.
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.FileField.upload_to