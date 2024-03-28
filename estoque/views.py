from django.shortcuts import render

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
    context = {}
    return render(request, 'estoque/pages/clientes.html', context)