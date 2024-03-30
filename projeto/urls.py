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
    path('', views.home, name='home'),
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

    #path('vendas/', views.categorias, name='categorias'),
    #path('vendas/criar', views.criar_categoria, name='criar_venda'),
    #path('vendas/buscar', views.buscar_categoria, name='buscar_venda'),
    #path('vendas/editar/', views.editar_categoria, name='editar_venda'),
    #path('vendas/editar/<int:categoria_id>/', views.remover_categoria, name='remover_venda'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
