from rest_framework import serializers
from .models import Produtos, Carrinho

class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'

class CarrinhoSerializer(serializers.ModelSerializer):
    produtos = serializers.PrimaryKeyRelatedField(many=True, queryset=Produtos.objects.all())

    class Meta:
        model = Carrinho
        fields = '__all__'
