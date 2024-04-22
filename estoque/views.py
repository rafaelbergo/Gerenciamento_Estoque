from datetime import datetime, timedelta
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from estoque.forms import BuscarClienteForm, BuscarVendaForm, VendaForm
from estoque.models import Cliente, Fornecedor, ItemVenda, Produto, Venda
from projeto import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
from django.db.models import Sum


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
    form = VendaForm()
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        data = request.POST.get('data')
        produto_id = request.POST.get('produto_id')
        quantidade = request.POST.get('quantidade')
        desconto = request.POST.get('desconto')
        forma_pagamento = request.POST.get('forma_pagamento')

        cliente = Cliente.objects.get(cpf=cpf)
        produto = Produto.objects.get(pk=produto_id)

        preco_unitario = produto.preco
        preco_total = int(quantidade) * float(preco_unitario)

        if desconto:
            preco_total = float(preco_total) * (1 - float(desconto) / 100)
        else:
            preco_total = preco_total

        venda = Venda(cliente=cliente, data=data, valor=preco_total, desconto=desconto, forma_pagamento=forma_pagamento)
        venda.save()

        item_venda = ItemVenda(venda=venda, produto=produto, quantidade=quantidade, valor_unitario=preco_unitario)
        item_venda.save()  

        # Atualiza o estoque do produto
        produto.quantidade -= int(quantidade)
        produto.save()

        return render(request, 'estoque/pages/vendas/criar-venda.html', {'form': form})
    else:
        return render(request, 'estoque/pages/vendas/criar-venda.html', {'form': form})
    

def calcular_preco_final(venda):
    total = 0
    for item in venda.itemvenda_set.all():
        total += item.quantidade * item.produto.preco
    if venda.desconto:
        total -= total * (venda.desconto / 100)
    return round(total, 2)


def buscar_venda(request):
    form = BuscarVendaForm(request.GET)
    vendas = []

    if form.is_valid():
        campo = form.cleaned_data['campo']
        valor = form.cleaned_data['valor']

        if campo == 'todos':
            vendas = Venda.objects.all().prefetch_related('itemvenda_set')
        else:
            if campo and valor:
                filtros = {
                    'id': Venda.objects.filter(id=valor),
                    'cpf': Venda.objects.filter(cliente__cpf__icontains=valor),
                    'data': Venda.objects.filter(data__icontains=valor),
                    'forma_pagamento': Venda.objects.filter(forma_pagamento__icontains=valor),
                }
                vendas = filtros.get(campo, []).prefetch_related('itemvenda_set')

    for venda in vendas:
        venda.preco_final = calcular_preco_final(venda)

    contexto = {'form': form, 'vendas': vendas, 'opcoes': form.fields['campo'].choices}

    return render(request, 'estoque/pages/vendas/buscar-venda.html', contexto)

def relatorios_vendas(request):
    context = {}
    if request.method == 'POST':
        periodo = request.POST.get('periodo')
        if periodo:
            context['relatorio_tipo'] = 'vendas_diarias'
            vendas_queryset = calcular_relatorio(periodo)  # Obtendo a queryset de vendas
            quantidade_vendas = vendas_queryset.count() if vendas_queryset else 0
            context['relatorio'] = vendas_queryset
            context['quantidade_vendas'] = quantidade_vendas
            
    return render(request, 'estoque/pages/vendas/relatorios-vendas.html', context)

def calcular_relatorio(periodo):
    data_atual = datetime.now().date()
    if periodo == 'dia_atual':
        vendas = Venda.objects.filter(data=data_atual).annotate(total_vendas=Sum('valor'))
    elif periodo == 'ultimos_7_dias':
        data_inicio = data_atual - timedelta(days=7)
        vendas = Venda.objects.filter(data__range=[data_inicio, data_atual]).annotate(total_vendas=Sum('valor'))
    elif periodo == 'ultimos_30_dias':
        data_inicio = data_atual - timedelta(days=30)
        vendas = Venda.objects.filter(data__range=[data_inicio, data_atual]).annotate(total_vendas=Sum('valor'))
    elif periodo == 'ultimos_365_dias':
        data_inicio = data_atual - timedelta(days=365)
        vendas = Venda.objects.filter(data__range=[data_inicio, data_atual]).annotate(total_vendas=Sum('valor'))
    else:
        vendas = Venda.objects.none()
    return vendas


def fornecedores(request):
    total_fornecedores = Fornecedor.objects.all().count()
    context = {'total_fornecedores': total_fornecedores}
    return render(request, 'estoque/pages/fornecedores/fornecedores.html', context)

def criar_fornecedor(request):
    mensagem = None
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        cep = request.POST.get('cep')
        
        if nome and cnpj:
            novo_fornecedor = Fornecedor.objects.create(
                nome=nome,
                cnpj=cnpj,
                email=email,
                telefone=telefone,
                endereco=endereco,
                cidade=cidade,
                estado=estado,
                cep=cep
            )
            mensagem = "Fornecedor criado com sucesso!"
        else:
            mensagem = "Nome e CNPJ são campos obrigatórios."

    return render(request, 'estoque/pages/fornecedores/criar-fornecedor.html', {'mensagem': mensagem})

def buscar_fornecedor(request):
    campo = request.GET.get('campo')
    valor = request.GET.get('valor')

    if campo == 'todos':
        fornecedores = Fornecedor.objects.all()
    else:
        if campo and valor:
            filtros = {
                'id': Fornecedor.objects.filter(id=valor),
                'nome': Fornecedor.objects.filter(nome__icontains=valor),
                'cnpj': Fornecedor.objects.filter(cnpj__icontains=valor),
                'email': Fornecedor.objects.filter(email__icontains=valor),
                'telefone': Fornecedor.objects.filter(telefone__icontains=valor),
                'endereco': Fornecedor.objects.filter(endereco__icontains=valor),
                'cidade': Fornecedor.objects.filter(cidade__icontains=valor),
                'estado': Fornecedor.objects.filter(estado__icontains=valor),
                'cep': Fornecedor.objects.filter(cep__icontains=valor),
            }
            fornecedores = filtros.get(campo, [])
     
        else:
            fornecedores = []

    campos_opcoes = {
        'todos': 'Todos os fornecedores',
        'id': 'ID',
        'nome': 'Nome',
        'cnpj': 'CNPJ',
        'email': 'E-mail',
        'telefone': 'Telefone',
        'endereco': 'Endereço',
        'cidade': 'Cidade',
        'estado': 'Estado',
        'cep': 'CEP',    
    }

    contexto = {'fornecedores': fornecedores, 'campo': campo, 'valor': valor}

    contexto['opcoes'] = campos_opcoes
    contexto['campo'] = campo if campo in campos_opcoes else 'todos'

    return render(request, 'estoque/pages/fornecedores/buscar-fornecedor.html', contexto)

def editar_fornecedor(request):
    fornecedor = None
    sucesso = False
    if request.method == 'POST':
        fornecedor_id = request.POST.get('fornecedor_id')
        if fornecedor_id:
            fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
        else:
            fornecedor_id = request.POST.get('fornecedor_id_hidden')
            fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
            fornecedor.nome = request.POST.get('nome')
            fornecedor.email = request.POST.get('email')
            fornecedor.cnpj = request.POST.get('cnpj')
            fornecedor.telefone = request.POST.get('telefone')
            fornecedor.endereco = request.POST.get('endereco')
            fornecedor.cidade = request.POST.get('cidade')
            fornecedor.estado = request.POST.get('estado')
            fornecedor.cep = request.POST.get('cep')
            fornecedor.save()
            sucesso = True
            fornecedor = None

    return render(request, 'estoque/pages/fornecedores/editar-fornecedor.html', {'fornecedor': fornecedor, 'sucesso': sucesso})

def remover_fornecedor(request, fornecedor_id):
    deletado = False

    if request.method == 'POST':
        fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
        fornecedor.delete()
        deletado = True

    return render(request, 'estoque/pages/fornecedores/editar-fornecedor.html', {'deletado': deletado})