"""
URL configuration for projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from estoque import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.produtos, name='produtos'),
    # path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/criar', views.criar_cliente, name='criar_cliente'),
    path('clientes/buscar', views.buscar_cliente, name='buscar_cliente'),
    path('clientes/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.remover_cliente, name='remover_cliente'),

    path('produtos/', views.produtos, name='produtos'),
    path('produtos/criar', views.criar_produto, name='criar_produto'),
    path('produtos/buscar', views.buscar_produto, name='buscar_produto'),
    path('produtos/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/editar/<int:produto_id>/', views.remover_produto, name='remover_produto'),
    path('produtos/relatorios', views.relatorios_produtos, name='relatorios_produtos'),

    path('vendas/', views.vendas, name='vendas'),
    path('vendas/criar', views.criar_venda, name='criar_venda'),
    path('buscar-cliente-venda/', views.buscar_cliente_venda, name='buscar_cliente_venda'),
    path('buscar-produto-venda/', views.buscar_produto_venda, name='buscar_produto_venda'),
    path('vendas/buscar/', views.buscar_venda, name='buscar_venda'),
    path('vendas/relatorios', views.relatorios_vendas, name='relatorios_vendas'),

    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/criar', views.criar_fornecedor, name='criar_fornecedor'),
    path('fornecedores/buscar', views.buscar_fornecedor, name='buscar_fornecedor'),
    path('fornecedores/editar/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/editar/<int:fornecedor_id>/', views.remover_fornecedor, name='remover_fornecedor'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
