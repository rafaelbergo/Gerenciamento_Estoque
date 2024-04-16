import datetime
from django import forms


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
    cpf = forms.CharField(label='CPF do Cliente', max_length=14, widget=forms.TextInput(attrs={'placeholder': 'XXX.XXX.XXX-XX', 'pattern': '[0-9]{11}', 'title': 'Digite apenas números'}))
    nome_cliente = forms.CharField(label='Nome do Cliente', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    endereco = forms.CharField(label='Endereço', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    cep = forms.CharField(label='CEP', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    buscar_cliente = forms.CharField(label='', widget=forms.HiddenInput(), required=False)

    

    # Dados da venda
    data = forms.DateField(label='Data', widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today)
    valor = forms.DecimalField(label='Valor', min_value=0, decimal_places=2)



    #forma_pagamento = forms.ChoiceField(label='Forma de Pagamento', choices=OPCOES_PAGAMENTO)
    #produtos = forms.ModelMultipleChoiceField(label='Produtos', queryset=Produto.objects.all())
    #quantidades = forms.IntegerField(label='Quantidades', min_value=1)
    #valores_unitarios = forms.DecimalField(label='Valores Unitários', min_value=0, decimal_places=2)