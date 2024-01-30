from django.contrib import admin
from .models import (Produtos, Carrinho, RelatorioEntradaSaida, 
                     Saida, Pedido, Acai, Caldas, Cremes, Frutas, 
                     Adicionais, Outros)

admin.site.register(Carrinho)

admin.site.register(Produtos)
admin.site.register(RelatorioEntradaSaida)
admin.site.register(Saida)
admin.site.register(Pedido)

admin.site.register(Acai)
admin.site.register(Caldas)
admin.site.register(Cremes)
admin.site.register(Frutas)
admin.site.register(Adicionais)
admin.site.register(Outros)