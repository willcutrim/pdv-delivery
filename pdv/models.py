from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Produtos(models.Model):

    nome_produto = models.CharField(max_length=150)
    preco_do_produto = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()


    def __str__(self) -> str:
        return self.nome_produto
    

class Carrinho(models.Model):
    status_entrada = models.CharField(max_length=120, default='entrada')
    produtos = models.ManyToManyField(Produtos)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_compra = models.DateTimeField(auto_now_add=True)


    # def calcular_valor_total(self):
    #     self.valor_total = sum(item.preco_total() for item in self.itens.all())
    #     self.save()


    # def limpar_carrinho(self):
    #     self.itens.all().delete()
    #     self.calcular_valor_total()

    def __str__(self):
        return f'Carrinho #{self.produtos}'
    

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
    tipo = models.CharField(max_length=150)
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    data = models.DateTimeField(auto_now_add=True)

    
    def data_log_formatada(self):
        return self.data.strftime('%d/%m/%Y')

    def __str__(self):
        return f"{self.tipo} - {self.data.strftime('%d/%m/%Y')}"


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
            tipo=instance.status_entrada,
            descricao=instance.produtos,
            valor=instance.valor_total,
            data=instance.data_compra
        )
