from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('relatorio-entrada-saida', views.relatorio_entrada_saida_view, name='relatorio-entrada-saida'),

    path('cadastro_saida', views.cadastro_saida, name='cadastro-saida'),
    path('deletar_entrada_saida<int:id>', views.deletar_relatorio, name='deletar-entrada-saida'),

    path('realizar_pedido_cliente', views.pedido_whatsapp, name='realizar-pedido-cliente'),

    path('pedidos-feitos', views.pedidos_feitos, name='pedidos-feitos'),

    path('deletar-pedido/<int:id>', views.deletar_pedidos, name='deletar-pedido'),

    path('login', views.login_page, name='login'),
    path('logout', views.logout_django, name='logout'),

    path('relatorio-saidas', views.relatorio_saida, name='relatorio-saidas'),

    path('realizar-pedido', views.realizar_pedido_sistema, name='realizar-pedido')
]
