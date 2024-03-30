import os
from django.shortcuts import get_object_or_404, redirect, render
from estoque.models import Cliente, Produto

def home(request):
    context = {}
    return render(request, 'estoque/pages/home.html', context)

def categorias(request):
    context = {}
    return render(request, 'estoque/pages/categorias.html', context)

def clientes(request):
    total_clientes = Cliente.objects.all().count()
    context = {'total_clientes': total_clientes}
    return render(request, 'estoque/pages/clientes/clientes.html', context)

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

    return render(request, 'estoque/pages/clientes/criar-cliente.html', {'mensagem': mensagem})

def buscar_cliente(request):
    campo = request.GET.get('campo')
    valor = request.GET.get('valor')

    if campo == 'todos':
        clientes = Cliente.objects.all()
    else:
        if campo and valor:
            filtros = {
                'id': Cliente.objects.filter(id=valor),
                'nome': Cliente.objects.filter(nome__icontains=valor),
                'cpf': Cliente.objects.filter(cpf__icontains=valor),
                'email': Cliente.objects.filter(email__icontains=valor),
                'telefone': Cliente.objects.filter(telefone__icontains=valor),
                'endereco': Cliente.objects.filter(endereco__icontains=valor),
                'cidade': Cliente.objects.filter(cidade__icontains=valor),
                'estado': Cliente.objects.filter(estado__icontains=valor),
                'cep': Cliente.objects.filter(cep__icontains=valor),
            }
            clientes = filtros.get(campo, [])
     
        else:
            clientes = []

    campos_opcoes = {
        'todos': 'Todos os clientes',
        'id': 'ID',
        'nome': 'Nome',
        'cpf': 'CPF',
        'email': 'Email',
        'telefone': 'Telefone',
        'endereco': 'Endereço',
        'cidade': 'Cidade',
        'estado': 'Estado',
        'cep': 'CEP',
    }

    contexto = {'clientes': clientes, 'campo': campo, 'valor': valor}

    contexto['opcoes'] = campos_opcoes
    contexto['campo'] = campo if campo in campos_opcoes else 'todos'

    return render(request, 'estoque/pages/clientes/buscar-cliente.html', contexto)

def editar_cliente(request):
    cliente = None
    sucesso = False
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        if cliente_id:
            cliente = get_object_or_404(Cliente, id=cliente_id)
        else:
            cliente_id = request.POST.get('cliente_id_hidden')
            cliente = get_object_or_404(Cliente, id=cliente_id)
            cliente.nome = request.POST.get('nome')
            cliente.email = request.POST.get('email')
            cliente.cpf = request.POST.get('cpf')
            cliente.telefone = request.POST.get('telefone')
            cliente.endereco = request.POST.get('endereco')
            cliente.cidade = request.POST.get('cidade')
            cliente.estado = request.POST.get('estado')
            cliente.cep = request.POST.get('cep')
            cliente.save()
            sucesso = True
            cliente = None

    return render(request, 'estoque/pages/clientes/editar-cliente.html', {'cliente': cliente, 'sucesso': sucesso})

def remover_cliente(request, cliente_id):
    deletado = False

    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()
        deletado = True

    return render(request, 'estoque/pages/clientes/editar-cliente.html', {'deletado': deletado})

def produtos(request):
    total_produtos = Produto.objects.all().count()
    context = {'total_produtos': total_produtos}
    return render(request, 'estoque/pages/produtos/produtos.html', context)

def criar_produtos(request):
    mensagem = None
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        quantidade = request.POST.get('quantidade')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        imagem = request.FILES.get('imagem')
        
        if nome and preco and quantidade:
            novo_produto = Produto.objects.create(
                nome=nome,
                preco=preco,
                quantidade=quantidade,
                descricao=descricao,
                categoria=categoria,
                marca=marca,
                modelo=modelo,
            )

            if imagem:
                filename, extension = os.path.splitext(imagem.name)
                imagem.name = f'produtos/{novo_produto.id}{extension}'
                novo_produto.imagem = imagem
                novo_produto.save()
            
            mensagem = "Produto criado com sucesso!"
        else:
            mensagem = "Nome, preço e quantidade são campos obrigatórios."

    return render(request, 'estoque/pages/produtos/criar-produto.html', {'mensagem': mensagem})