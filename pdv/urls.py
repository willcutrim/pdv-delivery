from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastro_produtos', views.cadastrar_produtos, name="cadastrar-produtos"),
    path('relatorio_de_vendas', views.RelatorioDeVendasView.as_view(), name="relatorio-de-vendas"),
    path('caixa', views.CaixaView.as_view(), name="caixa"),
    path('lista_de_produtos', views.ListaProdutosView.as_view(), name="lista-de-produtos"),
    path('api/salvar-pedido/', views.CarrinhoListCreateView.as_view(), name='salvar-pedido'),
    path('api/get-price/', views.get_product_price, name='get_product_price'),
    path('relatorio-entrada-saida', views.RelatorioEntradaSaidaView.as_view(), name='relatorio-entrada-saida'),

    path('cadastro_saida', views.cadastro_saida, name='cadastro-saida'),
    path('deletar_entrada_saida<int:id>', views.deletar_relatorio, name='deletar-entrada-saida'),
    path('deletar_venda/<int:id>', views.deletar_venda, name='deletar-venda'),

    path('deletar_produto/<int:id>', views.deletar_produto, name='deletar-produto'),
    path('produto/<int:pk>/update/', views.ProdutoUpdateView.as_view(), name='editar-produto'),


]
