from django import forms

from .models import Product

# https://stackoverflow.com/questions/17948018/add-custom-form-fields-that-are-not-part-of-the-model-django


class WindowForm(forms.ModelForm):
    type_window = forms.CharField(label="Tipo de Janela")
    type_vedation = forms.CharField(label="Tipo de Vedação")
    has_mosquiteia = forms.BooleanField(label="Acompanha Tela Mosquiteira")

    class Meta:
        model = Product
        fields = "__all__"


# Marca
# Cor
# Tonalidade
# Material
# Produto
