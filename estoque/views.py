from django.shortcuts import render
from estoque.models import Cliente

def home(request):
    context = {}
    return render(request, 'estoque/pages/home.html', context)

def produtos(request):
    context = {}
    return render(request, 'estoque/pages/produtos.html', context)

def categorias(request):
    context = {}
    return render(request, 'estoque/pages/categorias.html', context)

def clientes(request):
    total_clientes = Cliente.objects.all().count()
    context = {'total_clientes': total_clientes}
    return render(request, 'estoque/pages/clientes.html', context)

def criar_cliente(request):
    context = {}
    return render(request, 'estoque/pages/criar-cliente.html', context)