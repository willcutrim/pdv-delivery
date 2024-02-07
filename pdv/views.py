from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .utils import converter_para_int, gerar_codigo_unico
from .forms import FormPedido, SaidaForm
from .models import Acai, Adicionais, Caldas, Cremes, Frutas, Outros, RelatorioEntradaSaida, Pedido, Saida
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import random
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta








@login_required(login_url="login")
def home_page(request):
    template_name = "html/home.html"
    return render(request, template_name)



    

# class CarrinhoListCreateView(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = CarrinhoSerializer(data=request.data)
#         print(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@login_required(login_url="login")
def relatorio_entrada_saida_view(request):
    template_name = "html/relatorio_entrada_saida.html"
    items_per_page = 10

    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')

    logs = RelatorioEntradaSaida.objects.all().order_by('-data')

    total_entradas = logs.filter(tipo='Entrada').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0

    qt_saidas = logs.filter(tipo='saida').count() or 0
    qt_entradas = logs.filter(tipo='Entrada').count() or 0

    if data_inicial_str:
        logs = logs.filter(data__date__gte=data_inicial_str)

        total_entradas = logs.filter(tipo='Entrada').aggregate(Sum('valor'))['valor__sum'] or 0
        total_saidas = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0

        qt_saidas = logs.filter(tipo='saida').count() or 0
        qt_entradas = logs.filter(tipo='Entrada').count() or 0

        total_entradas_mensal = logs.filter(tipo='Entrada').aggregate(Sum('valor'))['valor__sum'] or 0
        total_saidas_mensal = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0

        saldo_total = total_entradas_mensal - total_saidas

    if data_final_str:
        logs = logs.filter(data__date__lte=data_final_str)

        total_entradas = logs.filter(tipo='Entrada').aggregate(Sum('valor'))['valor__sum'] or 0
        total_saidas = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0

        qt_saidas = logs.filter(tipo='saida').count() or 0
        qt_entradas = logs.filter(tipo='Entrada').count() or 0

        total_entradas_mensal = logs.filter(tipo='Entrada').aggregate(Sum('valor'))['valor__sum'] or 0
        total_saidas_mensal = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0


        saldo_total = total_entradas_mensal - total_saidas

    total_entradas_mensal = logs.filter(tipo='Entrada').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_mensal = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0


    saldo_total = total_entradas_mensal - total_saidas

    # Paginação
    page_number = request.GET.get('page', 1)
    paginator = Paginator(logs, items_per_page)

    try:
        page_logs = paginator.page(page_number)
    except PageNotAnInteger:
        page_logs = paginator.page(1)
    except EmptyPage:
        page_logs = paginator.page(paginator.num_pages)
    
    context = {
        'logs': page_logs,
        'total_entradas': total_entradas,
        'total_entradas_mensal': total_entradas_mensal,
        'total_saidas_mensal': total_saidas_mensal,
        'total_saidas': total_saidas,
        'data_inicial': data_inicial_str,
        'data_final': data_final_str,
        'qt_saidas': qt_saidas,
        'qt_entradas': qt_entradas,
        'saldo': saldo_total,
    }

    return render(request, template_name, context)
    



@login_required(login_url="login")
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




@login_required(login_url="login")
def deletar_relatorio(request, id):
   
    if request.method == 'POST':    
        entrada_saida = get_object_or_404(RelatorioEntradaSaida, id=id)
        entrada_saida.delete()
        return redirect('relatorio-entrada-saida')
    




    
TAMANHO_VALORES = {
    '300 ML': 12,
    '400 ML': 15,
    '500 ML': 18,
    'Potão': 20,
}

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

        
        if tamanho_acai in TAMANHO_VALORES:
            pedido.valor_do_pedido = Decimal(TAMANHO_VALORES[tamanho_acai]) + Decimal(2)

        # Adiciona 2 ao valor total para cada adicional escolhido
        for adicional in objetos_adicionais:
            pedido.valor_do_pedido += Decimal(2)
       
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





@login_required(login_url="login")
def pedidos_feitos(request):

    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')
    
    pedidos = Pedido.objects.all().order_by('-create')
    pedidos_all = Pedido.objects.all().order_by('-create')
    
    

    if data_inicial_str and data_final_str:
        data_inicial = timezone.datetime.strptime(data_inicial_str, '%Y-%m-%d').date()
        data_final = timezone.datetime.strptime(data_final_str, '%Y-%m-%d').date() + timedelta(days=1)

        pedidos = pedidos.filter(create__date__gte=data_inicial, create__date__lt=data_final)

        valor_total_vendas = sum([converter_para_int(pedido.valor_do_pedido) for pedido in pedidos])
       

    valor_semanal = sum([converter_para_int(pedido.valor_do_pedido) for pedido in pedidos_all.filter(create__gte=timezone.now() - timedelta(days=7))])
    valor_diario = sum([converter_para_int(pedido.valor_do_pedido) for pedido in pedidos_all.filter(create__date=timezone.now().date())])

    valor_total_vendas = sum([converter_para_int(pedido.valor_do_pedido) for pedido in pedidos])


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
        'count_pedidos': pedidos_all,
        'data_inicial': data_inicial_str,
        'data_final': data_final_str,
        'valor_total_vendas': valor_total_vendas,
        'valor_semanal': valor_semanal,
        'valor_diario': valor_diario,
    }
    return render(request, 'html/pedidos_feitos.html', context)




@login_required(login_url="login")
def deletar_pedidos(request, id):

    if request.method == 'POST':    
        pedido = get_object_or_404(Pedido, id=id)
        pedido.delete()
        return redirect('pedidos-feitos')
    


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and check_password(password, user.password):
                login(request, user)
                print(username, password)
                return redirect('home')
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    return render(request, 'html/login.html')




def logout_django(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('login')
    


def relatorio_saida(request):

    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')

    saidas = Saida.objects.all().order_by('-data_saida')
    return render(request, 'html/saidas.html', {'saidas':saidas}) 



def realizar_pedido_sistema(request):
    tamanho_acai = Acai.objects.all()
    if request.method == 'POST':
        form = FormPedido(request.POST)
        if form.is_valid():
            valor_do_pedido = form.cleaned_data.get('valor_do_pedido')
            nome = form.cleaned_data.get('nome')
            tamanho_acai = form.cleaned_data.get('tamanho_acai')
            forma_de_pagamento = form.cleaned_data.get('forma_de_pagamento')

            codigo_do_pedido = gerar_codigo_unico()


            pedido = Pedido(
                codigo_do_pedido=codigo_do_pedido,
                valor_do_pedido=valor_do_pedido,
                nome=nome,
                forma_de_pagamento=forma_de_pagamento,
                tamanho_acai=tamanho_acai,
            )

            pedido.save()
            return redirect('realizar-pedido')
        
    else:
        form = FormPedido()
    return render(request, 'html/pedido_no_sistema.html', {'form': form, 'tamanho_acai': tamanho_acai})
