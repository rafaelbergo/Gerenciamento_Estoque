import datetime
from django import forms

from estoque.models import Produto


class BuscarClienteForm(forms.Form):
    campo = forms.ChoiceField(choices=[
        ('todos', 'Todos os clientes'),
        ('id', 'ID'),
        ('nome', 'Nome'),
        ('cpf', 'CPF'),
        ('email', 'Email'),
        ('telefone', 'Telefone'),
        ('endereco', 'Endereço'),
        ('cidade', 'Cidade'),
        ('estado', 'Estado'),
        ('cep', 'CEP'),
    ])
    valor = forms.CharField(required=False)


class VendaForm(forms.Form):
    # Dados do cliente
    cpf = forms.CharField(label='CPF do Cliente', max_length=14, required=True, widget=forms.TextInput(attrs={'placeholder': 'XXX.XXX.XXX-XX', 'pattern': '[0-9]{11}', 'title': 'Digite apenas números'}))
    nome_cliente = forms.CharField(label='Nome do Cliente', required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': True}))
    endereco = forms.CharField(label='Endereço', required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': True}))
    cep = forms.CharField(label='CEP', required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': True}))
    buscar_cliente = forms.CharField(label='', widget=forms.HiddenInput(), required=False)

    # Dados dos produtos
    produto_id = forms.IntegerField(label='ID do Produto', required=True)
    produto_nome = forms.CharField(label='Nome do Produto', required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': True}))
    produto_preco = forms.DecimalField(label='Preço do Produto', required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': True}))
    produto_estoque = forms.IntegerField(label='Quantidade em Estoque', required=False, disabled=True, widget=forms.TextInput(attrs={'readonly': True}))
    
    # Dados da venda
    data = forms.DateField(label='Data', widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today)
    quantidade = forms.IntegerField(label='Quantidade', min_value=1, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    preco_total = forms.DecimalField(label='Preço Total', decimal_places=2, disabled=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    desconto = forms.DecimalField(label='Desconto em %', decimal_places=3, required=True, min_value=0, max_value=100,widget=forms.NumberInput(attrs={'class': 'form-control'}))
    opcoes_pagamento = (
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CARTAO', 'Cartão'),
    )
    forma_pagamento = forms.ChoiceField(label='Forma de Pagamento', choices=opcoes_pagamento)