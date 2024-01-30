from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from .forms import ProdutosForm, SaidaForm, FormPedido
from .models import Acai, Adicionais, Caldas, Cremes, Frutas, Outros, Produtos, Carrinho, RelatorioEntradaSaida, Saida, Pedido
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializer import CarrinhoSerializer
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views.generic.edit import UpdateView
from django.utils import timezone
import random
import time




class HomeView(TemplateView):
    template_name = "html/home.html"



def cadastrar_produtos(request):
    if request.method == 'POST':
        form = ProdutosForm(request.POST)
        if form.is_valid():
            nome_produto = form.cleaned_data['nome_produto']
            produto = Produtos.objects.filter(nome_produto=nome_produto).first()

            if produto is not None:
                response_data = {'erro': 'Já existe um produto com esse nome!'}
                
            else:
                form.save()
                response_data = {'success': 'Produto cadastrado com sucesso!'}
            print(response_data)
            return JsonResponse(response_data)

        else:
           
            errors = form.errors.as_json()
            return JsonResponse({'erro': errors})
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
    

class CarrinhoListCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CarrinhoSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



def get_product_price(request):
    
    pk_product = request.GET.get('product')

    try:
        product = Produtos.objects.get(nome_produto=pk_product)
        price = product.preco_do_produto
        return JsonResponse({'preco_do_produto': price})
    except Produtos.DoesNotExist:
        return JsonResponse({'preco': 0.00})
    

class RelatorioEntradaSaidaView(TemplateView):
    template_name = "html/relatorio_entrada_saida.html"
    items_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data_inicial_str = self.request.GET.get('data_inicial')
        data_final_str = self.request.GET.get('data_final')

        logs = RelatorioEntradaSaida.objects.all().order_by('-data')

        total_entradas = RelatorioEntradaSaida.objects.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum']
        total_saidas = RelatorioEntradaSaida.objects.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum']


        qt_saidas = RelatorioEntradaSaida.objects.filter(tipo='saida')
        qt_entradas = RelatorioEntradaSaida.objects.filter(tipo='entrada')

        if data_final_str:
            logs = logs.filter(data__date__gte=data_inicial_str)
        if data_final_str:
            logs = logs.filter(data__date__lte=data_final_str)

        total_entradas_mensal = logs.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum']
        total_saidas_mensal = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum']

        # Pagination
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(logs, self.items_per_page)

        try:
            page_logs = paginator.page(page_number)
        except PageNotAnInteger:
            page_logs = paginator.page(1)
        except EmptyPage:
            page_logs = paginator.page(paginator.num_pages)
       
       
        context['logs'] = page_logs
        context['total_entradas'] = total_entradas or 0
        context['total_entradas_mensal'] = total_entradas_mensal or 0
        context['total_saidas_mensal'] = total_saidas_mensal or 0
        context['total_saidas'] = total_saidas or 0
        context['data_inicial'] = data_inicial_str
        context['data_final'] = data_final_str
        context['qt_saidas'] = qt_saidas or 0
        context['qt_entradas'] = qt_entradas or 0

        return context
    

def cadastro_saida(request):

    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': 'Produto cadastrado com sucesso!'}
            return JsonResponse(response_data)
        
    else:
        form = SaidaForm()
    return render(request, 'html/cadastro_saidas.html', {'form': form})



class ProdutoUpdateView(UpdateView):
    model = Produtos
    form_class = ProdutosForm
    template_name = 'html/editar_produto.html'
    success_url = '/lista_de_produtos'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)



def deletar_relatorio(request, id):
   
    if request.method == 'POST':    
        entrada_saida = get_object_or_404(RelatorioEntradaSaida, id=id)
        entrada_saida.delete()
        return redirect('relatorio-entrada-saida')
    

def deletar_venda(request, id):
   
    if request.method == 'POST':    
        vendas = get_object_or_404(Carrinho, id=id)
        vendas.delete()
        return redirect('relatorio-de-vendas')
    
def deletar_produto(request, id):
   
    if request.method == 'POST':    
        produto = get_object_or_404(Produtos, id=id)
        produto.delete()
        return redirect('lista-de-produtos')
    


def pedido_whatsapp(request):
    
    if request.method == 'POST':

        tamanho_acai = request.POST.get('tamanho', '')
        caldas = request.POST.getlist('caldas', [])
        cremes = request.POST.getlist('creme', [])
        frutas = request.POST.getlist('fruta', [])
        outros = request.POST.getlist('outros', [])
        adicionais = request.POST.getlist('adicionais', [])
        bairro = request.POST.get('bairro', '')
        rua = request.POST.get('rua', '')
        numero_da_casa = request.POST.get('numero_da_casa', '')
        complemento = request.POST.get('complemento', '')
        nome = request.POST.get('nome', '')
        forma_de_pagamento = request.POST.get('formaDePagamento', '')
        dinheiro_valor = request.POST.get('dinheiro_valor', '')

        codigo_do_pedido = gerar_codigo_unico()

        objetos_adicionais = [Adicionais.objects.create(nome=nome_adicional) for nome_adicional in adicionais]

        pedido = Pedido(
            codigo_do_pedido=codigo_do_pedido,
            tamanho_acai=tamanho_acai,
            bairro=bairro,
            rua=rua,
            numero_da_casa=numero_da_casa,
            complemento=complemento,
            nome=nome,
            forma_de_pagamento=forma_de_pagamento,
            dinheiro_valor=dinheiro_valor
        )
       
        print(adicionais)
       
        pedido.save()

        pedido.caldas.set(Caldas.objects.filter(nome__in=caldas))
        pedido.creme.set(Cremes.objects.filter(nome__in=cremes))
        pedido.fruta.set(Frutas.objects.filter(nome__in=frutas))
        pedido.outros.set(Outros.objects.filter(nome__in=outros))
        pedido.adicionais.set(objetos_adicionais)


    context = {
        'tamanho_acai': Acai.objects.all(), 
        'caldas':  Caldas.objects.all(),
        'cremes':  Cremes.objects.all(),
        'frutas': Frutas.objects.all(),
        'outros': Outros.objects.all(),
    }
    return render(request, 'html/realizar_pedido_whatsapp.html', context)




def gerar_codigo_unico():
    codigo = random.randint(10000, 99999)
    while Pedido.objects.filter(codigo_do_pedido=codigo).exists():
        codigo = random.randint(10000, 99999)
    return codigo


def pedidos_feitos(request):

    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')
    
    pedidos = Pedido.objects.all().order_by('-create')


    if data_final_str:
        pedidos = pedidos.filter(create__date__gte=data_inicial_str)
    if data_final_str:
        pedidos = pedidos.filter(create__date__lte=data_final_str)

    paginator = Paginator(pedidos, 10)
    page = request.GET.get('page')
    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)

    context = {
        'pedidos': pedidos,
        'data_inicial': data_inicial_str,
        'data_final': data_final_str
    }
    return render(request, 'html/pedidos_feitos.html', context)


def deletar_pedidos(request, id):

    if request.method == 'POST':    
        pedido = get_object_or_404(Pedido, id=id)
        pedido.delete()
        return redirect('pedidos-feitos')