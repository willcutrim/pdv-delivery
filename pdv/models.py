from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import ProtectedError



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
    # preco_do_acai = models.DecimalField(decimal_places=2, max_digits=10)

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
class Outros(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Adicionais(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    adicionais_relacionados = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    saida_status = models.CharField(max_length=120, default='Entrada')
    codigo_do_pedido = models.CharField(max_length=10, unique=True)
    valor_do_pedido = models.CharField(max_length=255, blank=True, null=True,  verbose_name="Valor total do pedido")
    tamanho_acai = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tamanho do açai")
    caldas = models.ManyToManyField(Caldas, blank=True)
    creme = models.ManyToManyField(Cremes, blank=True)
    fruta = models.ManyToManyField(Frutas, blank=True)
    outros = models.ManyToManyField(Outros, blank=True)
    adicionais = models.ManyToManyField(Adicionais, blank=True)
    bairro = models.CharField(max_length=255)
    rua = models.CharField(max_length=255)
    numero_da_casa = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    nome = models.CharField(max_length=255, verbose_name="Nome do cliente")
    forma_de_pagamento = models.CharField(max_length=255, verbose_name="Forma de pagamento")
    dinheiro_valor = models.CharField(max_length=255, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.codigo_do_pedido



@receiver(post_save, sender=Saida)
def create_relatorio_entrada_saida_saida(sender, instance, created, **kwargs):
    if created:
        RelatorioEntradaSaida.objects.create(
            id_movimento=instance.pk,
            tipo=instance.saida_status,
            descricao=instance.tipo_de_despesa,
            valor=instance.valor_despesa,
            data=instance.data_saida
        )


@receiver(post_save, sender=Pedido)
def create_relatorio_entrada_(sender, instance, created, **kwargs):
    if created:
        RelatorioEntradaSaida.objects.create(
            id_movimento=instance.pk,
            tipo=instance.saida_status,
            descricao='Venda',
            valor=instance.valor_do_pedido,
            data=instance.create
        )


@receiver(pre_delete, sender=RelatorioEntradaSaida)
def delete_related_pedido(sender, instance, **kwargs):
    try:
        pedido = Pedido.objects.get(id=instance.id_movimento, saida_status='Entrada')
        pre_delete.disconnect(delete_related_relatorio, sender=Pedido)
        pedido.delete()
    except (Pedido.DoesNotExist, ProtectedError):
        pass # algum dia eu trato esse error
    finally:
        pre_delete.connect(delete_related_relatorio, sender=Pedido)

@receiver(pre_delete, sender=Pedido)
def delete_related_relatorio(sender, instance, **kwargs):
    try:
        relatorio = RelatorioEntradaSaida.objects.get(id_movimento=instance.pk, tipo='Entrada')
        pre_delete.disconnect(delete_related_pedido, sender=RelatorioEntradaSaida)
        relatorio.delete()
    except (RelatorioEntradaSaida.DoesNotExist, ProtectedError):
        pass # algum dia eu trato esse error(Deus abençoe)
    finally:
        pre_delete.connect(delete_related_pedido, sender=RelatorioEntradaSaida)