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
    mensagem = None
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        cep = request.POST.get('cep')
        
        if nome and cpf:
            novo_cliente = Cliente.objects.create(
                nome=nome,
                cpf=cpf,
                email=email,
                telefone=telefone,
                endereco=endereco,
                cidade=cidade,
                estado=estado,
                cep=cep
            )
            mensagem = "Cliente criado com sucesso!"
        else:
            mensagem = "Nome e CPF são campos obrigatórios."
            
    return render(request, 'estoque/pages/criar-cliente.html', {'mensagem': mensagem})
