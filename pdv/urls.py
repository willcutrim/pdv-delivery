from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastro_produtos', views.cadastrar_produtos, name="cadastrar-produtos"),
    path('relatorio_de_vendas', views.RelatorioDeVendasView.as_view(), name="relatorio-de-vendas"),
    path('caixa', views.CaixaView.as_view(), name="caixa"),
    path('lista_de_produtos', views.ListaProdutosView.as_view(), name="lista-de-produtos"),
    path('api/salvar-pedido/', views.CarrinhoListCreateView.as_view(), name='salvar-pedido'),

]
