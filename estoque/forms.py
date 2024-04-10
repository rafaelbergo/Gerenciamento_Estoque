import datetime
from django import forms

class VendaForm(forms.Form):
    cpf = forms.CharField(label='CPF do Cliente', max_length=14, widget=forms.TextInput(attrs={'placeholder': 'XXX.XXX.XXX-XX', 'pattern': '[0-9]{11}', 'title': 'Digite apenas números'}))
    data = forms.DateField(label='Data', widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.date.today)
    valor = forms.DecimalField(label='Valor', min_value=0, decimal_places=2)
    #forma_pagamento = forms.ChoiceField(label='Forma de Pagamento', choices=OPCOES_PAGAMENTO)
    #produtos = forms.ModelMultipleChoiceField(label='Produtos', queryset=Produto.objects.all())
    #quantidades = forms.IntegerField(label='Quantidades', min_value=1)
    #valores_unitarios = forms.DecimalField(label='Valores Unitários', min_value=0, decimal_places=2)