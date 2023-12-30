from rest_framework import serializers
from .models import Produtos, Carrinho

class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'

class CarrinhoSerializer(serializers.ModelSerializer):
    produtos = ProdutosSerializer(many=True, read_only=True)

    class Meta:
        model = Carrinho
        fields = ['id', 'status_entrada', 'produtos', 'valor_total', 'data_compra']
