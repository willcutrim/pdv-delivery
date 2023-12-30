from django.contrib import admin
from .models import Produtos, Carrinho, RelatorioEntradaSaida, Saida

admin.site.register(Carrinho)

admin.site.register(Produtos)
admin.site.register(RelatorioEntradaSaida)
admin.site.register(Saida)