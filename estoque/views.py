import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from estoque.forms import BuscarClienteForm, VendaForm
from estoque.models import Cliente, ItemVenda, Produto, Venda
from projeto import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
    form = BuscarClienteForm(request.GET)
    clientes = []

    if form.is_valid():
        campo = form.cleaned_data['campo']
        valor = form.cleaned_data['valor']

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

    contexto = {'form': form, 'clientes': clientes, 'opcoes': form.fields['campo'].choices}

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

def criar_produto(request):
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

def buscar_produto(request):
    campo = request.GET.get('campo')
    valor = request.GET.get('valor')

    if campo == 'todos':
        produtos = Produto.objects.all()
    else:
        if campo and valor:
            filtros = {
                'id': Produto.objects.filter(id=valor),
                'nome': Produto.objects.filter(nome__icontains=valor),
                'preco': Produto.objects.filter(preco__icontains=valor),
                'quantidade': Produto.objects.filter(quantidade__icontains=valor),
                'descricao': Produto.objects.filter(descricao__icontains=valor),
                'categoria': Produto.objects.filter(categoria__icontains=valor),
                'marca': Produto.objects.filter(marca__icontains=valor),
                'modelo': Produto.objects.filter(modelo__icontains=valor),
            }
            produtos = filtros.get(campo, [])
     
        else:
            produtos = []

    campos_opcoes = {
        'todos': 'Todos os produtos',
        'id': 'ID',
        'nome': 'Nome',
        'preco': 'Preço',
        'quantidade': 'Quantidade',
        'descricao': 'Descrição',
        'categoria': 'Categoria',
        'marca': 'Marca',
        'modelo': 'Modelo',    
    }

    contexto = {'produtos': produtos, 'campo': campo, 'valor': valor}

    contexto['opcoes'] = campos_opcoes
    contexto['campo'] = campo if campo in campos_opcoes else 'todos'

    response = render(request, 'estoque/pages/produtos/buscar-produto.html', contexto)
    response['Cache-Control'] = 'must-revalidate'
    return response
    #return render(request, 'estoque/pages/produtos/buscar-produto.html', contexto)

def editar_produto(request):
    produto = None
    sucesso = False
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        if produto_id:
            produto = get_object_or_404(Produto, id=produto_id)
        else:
            produto_id = request.POST.get('produto_id_hidden')
            produto = get_object_or_404(Produto, id=produto_id)
            produto.nome = request.POST.get('nome')
            produto.preco = request.POST.get('preco')
            produto.quantidade = request.POST.get('quantidade')
            produto.descricao = request.POST.get('descricao')
            produto.categoria = request.POST.get('categoria')
            produto.marca = request.POST.get('marca')
            produto.modelo = request.POST.get('modelo')
            imagem = request.FILES.get('imagem')

            if imagem:
                if produto.imagem: # Verifica se existe uma imagem
                    caminho_imagem = os.path.join(settings.MEDIA_ROOT, 'produtos', f'{produto_id}.png')
                    if os.path.exists(caminho_imagem): # Verifica se o arquivo da imagem existe
                        os.remove(caminho_imagem)
            
                nome_imagem = f'{produto_id}.png'
                caminho_imagem_nova = os.path.join(settings.MEDIA_ROOT, 'produtos', nome_imagem)
                default_storage.save(caminho_imagem_nova, ContentFile(imagem.read()))

                nome_imagem = f'{produto_id}.{imagem.name.split(".")[-1]}'  # ID_do_produto.formato
                caminho_imagem_nova = os.path.join(settings.MEDIA_ROOT, 'produtos', nome_imagem)
                default_storage.save(caminho_imagem_nova, imagem)
                
                # Atualize o campo 'imagem' do produto
                produto.imagem = os.path.join('produtos', nome_imagem)

            produto.save()
            sucesso = True
            produto = None

    return render(request, 'estoque/pages/produtos/editar-produto.html', {'produto': produto, 'sucesso': sucesso})

def remover_produto(request, produto_id):
    deletado = False

    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=produto_id)
        produto.delete()
        deletado = True

    return render(request, 'estoque/pages/produtos/editar-produto.html', {'deletado': deletado})

def relatorios_produtos(request):
    baixo_estoque = False
    quantidade_minima = None
    produtos_com_baixo_estoque = None

    if request.method == 'POST':
        quantidade_minima = request.POST.get('quantidade_minima')
        if quantidade_minima is not None:  
            baixo_estoque = True  
            produtos_com_baixo_estoque = Produto.objects.filter(quantidade__lte=quantidade_minima)

    context = {
        'baixo_estoque': baixo_estoque,
        'quantidade_minima': quantidade_minima,
        'produtos_com_baixo_estoque': produtos_com_baixo_estoque,
    }

    return render(request, 'estoque/pages/produtos/relatorios-produtos.html', context)


def vendas(request):
    total_vendas = Venda.objects.all().count()
    context = {'total_vendas': total_vendas}
    return render(request, 'estoque/pages/vendas/vendas.html', context)
'''

def criar_venda(request):
    mensagem = None

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        data = request.POST.get('data')
        valor = request.POST.get('valor')
        forma_pagamento = request.POST.get('forma_pagamento')
        produtos_ids = request.POST.getlist('produtos_ids')

        if cliente_id and data and valor and forma_pagamento and produtos_ids:
            # Criando a venda
            nova_venda = Venda.objects.create(
                cliente_id=cliente_id,
                data=data,
                valor=valor,
                forma_pagamento=forma_pagamento
            )

            # Adicionando os produtos à venda
            for produto_id in produtos_ids:
                item_venda = ItemVenda.objects.create(
                    venda=nova_venda,
                    produto_id=produto_id,
                    quantidade=1  # Defina a quantidade conforme necessário
                )

            mensagem = "Venda criada com sucesso!"
        else:
            mensagem = "Por favor, preencha todos os campos obrigatórios."

    context = {'mensagem': mensagem}
    return render(request, 'estoque/pages/vendas/criar-venda.html', context)
'''


def buscar_cliente_venda(request):
    if request.method == 'GET':
        cpf = request.GET.get('valor')
        if cpf:
            cliente = Cliente.objects.filter(cpf=cpf).first()
            if cliente:
                return JsonResponse({'nome_cliente': cliente.nome, 'endereco': cliente.endereco, 'cep': cliente.cep})
            else:
                return JsonResponse({'error': 'Cliente não encontrado'})
    return JsonResponse({'error': 'Requisição inválida'})


def buscar_produto_venda(request):
    if request.method == 'GET':
        produto_id = request.GET.get('id')
        if produto_id:
            produto = Produto.objects.get(pk=produto_id)
            if produto:
                return JsonResponse({'nome': produto.nome, 'preco': produto.preco, 'estoque': produto.quantidade})
            else:
                return JsonResponse({'error': 'Produto não encontrado'})
    return JsonResponse({'error': 'Requisição inválida'})


def criar_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            # Lógica para processar o formulário
            pass
    else:
        form = VendaForm()
    
    return render(request, 'estoque/pages/vendas/criar-venda.html', {'form': form})

