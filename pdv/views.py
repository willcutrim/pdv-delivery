from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import ProdutosForm
from .models import Produtos, Carrinho
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CarrinhoSerializer
from django.db.models import Sum
from rest_framework import generics

class HomeView(TemplateView):
    template_name = "html/home.html"


def cadastrar_produtos(request):

    if request.method == 'POST':
        form = ProdutosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar-produtos')
        
    else:
        form = ProdutosForm()
    return render(request, 'html/cadastro_produtos.html', {'form': form})



class RelatorioDeVendasView(TemplateView):
    template_name = "html/relatorio_de_vendas.html"

    items_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date_filter = self.request.GET.get('start_date', None)
        end_date_filter = self.request.GET.get('end_date', None)

        carrinhos = Carrinho.objects.all().order_by('-data_compra')
        
        if start_date_filter:
            carrinhos = carrinhos.filter(data_compra__date__gte=start_date_filter)
        if end_date_filter:
            carrinhos = carrinhos.filter(data_compra__date__lte=end_date_filter)

        
        total_value = carrinhos.aggregate(Sum('valor_total'))['valor_total__sum']

        paginator = Paginator(carrinhos, self.items_per_page)
        page = self.request.GET.get('page', 1)

        try:
            carrinhos = paginator.page(page)
        except PageNotAnInteger:
            carrinhos = paginator.page(1)
        except EmptyPage:
            carrinhos = paginator.page(paginator.num_pages)

        context['carrinhos'] = carrinhos
        context['paginator'] = paginator
        context['total_value'] = total_value 

        return context

class CaixaView(TemplateView):
    template_name = "html/caixa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        produtos = Produtos.objects.all()

        context['produtos'] = produtos

        return context
class ListaProdutosView(TemplateView):
    template_name = "html/lista_de_produtos.html"

    items_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        produtos_list = Produtos.objects.all()

        paginator = Paginator(produtos_list, self.items_per_page)
        page = self.request.GET.get('page', 1)

        try:
            produtos = paginator.page(page)
        except PageNotAnInteger:
            produtos = paginator.page(1)
        except EmptyPage:
            produtos = paginator.page(paginator.num_pages)

        context['produtos'] = produtos
        context['paginator'] = paginator

        return context
    


class CarrinhoListCreateView(generics.ListCreateAPIView):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer

    def perform_create(self, serializer):
        carrinho = serializer.save()
        carrinho.calcular_valor_total()
        carrinho.save()

    def list(self, request, *args, **kwargs):
        carrinhos = self.get_queryset()
        for carrinho in carrinhos:
            carrinho.calcular_valor_total()
            carrinho.save()

        return super().list(request, *args, **kwargs)
    

def get_product_price(request):
    
    pk_product = request.GET.get('product')

    try:
        product = Produtos.objects.get(pk=pk_product)
        price = product.preco_do_produto
        return JsonResponse({'preco_do_produto': price})
    except Produtos.DoesNotExist:
        return JsonResponse({'preco': 0.00})
    