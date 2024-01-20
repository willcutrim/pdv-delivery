from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Produtos(models.Model):

    nome_produto = models.CharField(max_length=150)
    preco_do_produto = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.nome_produto
    

class Carrinho(models.Model):
    status_entrada = models.CharField(max_length=120, default='entrada')
    produtos = models.ManyToManyField(Produtos)
    valor_total = models.DecimalField(decimal_places=2, max_digits=10, default=0, blank=True)
    data_compra = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Carrinho #{self.valor_total} - {self.data_compra}'
    

class Saida(models.Model):
    saida_status = models.CharField(max_length=120, default='saida')
    tipo_de_despesa = models.CharField(max_length=150, default='outras_despesas', verbose_name='Tipo de Despesa')
    valor_despesa = models.DecimalField(decimal_places=2, max_digits=10, default=0, blank=True, verbose_name='Valor da despesa')
    data_saida = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Saida'
        verbose_name_plural = 'Saidas'

    def __str__(self):
        return self.tipo_de_despesa
    

    def data_saida_formatada(self):
        return self.data_saida.strftime('%d/%m/%Y %H:%M')
    


class RelatorioEntradaSaida(models.Model):
    id_movimento = models.CharField(max_length=150)
    tipo = models.CharField(max_length=150)
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    data = models.DateTimeField(auto_now_add=True)

    
    def data_log_formatada(self):
        return self.data.strftime('%d/%m/%Y')

    def __str__(self):
        return f"{self.tipo} - {self.data.strftime('%d/%m/%Y')}"

class Acai(models.Model):
    tamaho_do_acai = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.tamaho_do_acai
class Caldas(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Cremes(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.nome
class Frutas(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.nome
class Adicionais(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome
class Pedido(models.Model):
    codigo_do_pedido = models.CharField(max_length=10, unique=True)
    tamanho_acai = models.CharField(max_length=255, blank=True, null=True)
    caldas = models.ManyToManyField(Caldas, blank=True)
    creme = models.ManyToManyField(Cremes, blank=True)
    fruta = models.ManyToManyField(Frutas, blank=True)
    adicionais = models.ManyToManyField(Adicionais, blank=True)
    bairro = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    numero_da_casa = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    forma_de_pagamento = models.CharField(max_length=255)
    dinheiro_valor = models.CharField(max_length=255, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Código do Pedido: {self.codigo_do_pedido}'

@receiver(post_save, sender=Saida)
def create_relatorio_entrada_saida_saida(sender, instance, created, **kwargs):
    if created:
        RelatorioEntradaSaida.objects.create(
            tipo=instance.saida_status,
            descricao=instance.tipo_de_despesa,
            valor=instance.valor_despesa,
            data=instance.data_saida
        )

    
@receiver(post_save, sender=Carrinho)
def create_relatorio_entrada_saida(sender, instance, created, **kwargs):
    if created:
        RelatorioEntradaSaida.objects.create(
            id_movimento=instance.id,
            tipo=instance.status_entrada,
            descricao='Venda',
            valor=instance.valor_total,
            data=instance.data_compra
        )
        

@receiver(pre_delete, sender=RelatorioEntradaSaida)
def delete_relatorio_entrada_saida(sender, instance, **kwargs):
    try:
        relatorio = Carrinho.objects.get(id=instance.id_movimento)
        relatorio.delete()
    except Carrinho.DoesNotExist:
        pass
    except Exception as e:
        #
        print(f"Erro ao excluir relatório: {e}")

@receiver(pre_delete, sender=Carrinho)
def delete_venda_entrada(sender, instance, **kwargs):
    try:
        relatorio = RelatorioEntradaSaida.objects.get(id_movimento=instance.id)
        relatorio.delete()
    except RelatorioEntradaSaida.DoesNotExist:
        pass
    except Exception as e:
        #
        print(f"Erro ao excluir relatório: {e}")