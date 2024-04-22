from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=45, blank=False)
    preco = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    quantidade = models.IntegerField(blank=False)
    descricao = models.TextField(max_length=100, blank=True)
    categoria = models.TextField(max_length=60, blank=True)
    marca = models.TextField(max_length=40, blank=True)
    modelo = models.CharField(max_length=255, blank=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True)
    fornecedor = models.ForeignKey('Fornecedor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome
  
class Cliente(models.Model):
    nome = models.CharField(max_length=30, blank=False)
    cpf = models.CharField(max_length=14, blank=False)
    email = models.EmailField(max_length=30, blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=45, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return self.nome
    
class Fornecedor(models.Model):
    nome = models.CharField(max_length=30, blank=False)
    cnpj = models.CharField(max_length=18, blank=False)
    email = models.EmailField(max_length=30, blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    endereco = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=45, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return self.nome
    
class Venda(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    produtos = models.ManyToManyField('Produto', through='ItemVenda')
    desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    opcoes_pagamento = (
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
        ('CARTAO', 'Cartão'),
    )
    forma_pagamento = models.CharField(max_length=45, blank=False, choices=opcoes_pagamento)

class ItemVenda(models.Model):
    venda = models.ForeignKey('Venda', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(blank=False)
    valor_unitario = models.DecimalField(max_digits=5, decimal_places=2, blank=False)