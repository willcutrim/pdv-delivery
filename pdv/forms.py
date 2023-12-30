from django import forms
from .models import Produtos


class ProdutosForm(forms.ModelForm):

    class Meta:
        model = Produtos
        fields = ('nome_produto', 'preco_do_produto', 'descricao',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome_produto'] = forms.CharField(
            label='Nome do produto',
            widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
        self.fields['preco_do_produto'] = forms.DecimalField(
            label='Preço do produto',
            widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
        self.fields['descricao'] = forms.CharField(
            label='Descrição do produto',
            widget=forms.Textarea(attrs={'class': 'form-control'}),
        )