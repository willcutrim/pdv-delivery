import datetime
from django import forms
from .models import Saida, Pedido



class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = ('tipo_de_despesa', 'valor_despesa',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['tipo_de_despesa'] = forms.CharField(
            label='Tipo de despesa',
            widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
        self.fields['valor_despesa'] = forms.DecimalField(
            label='Valor da despesa',
            widget=forms.NumberInput(attrs={'class': 'form-control'}),
        )



class FormPedido(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ('nome', 'tamanho_acai', 'forma_de_pagamento', 'valor_do_pedido')

