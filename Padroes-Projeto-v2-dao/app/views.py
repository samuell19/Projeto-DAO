from django.http import HttpResponseRedirect
from django.shortcuts import render
import sys

from django.urls import reverse
from utils import helper

from .dominio import *
from .dao import *


def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)


def categorias(request, acao=None, id=None):
    try:
        # DAO que utilizado neste metodo
        dao = CategoriaDAO()

        # listar registros 
        if acao is None:
            # define o comando SQL que será executado
            registros = dao.selecionar_todos()
            # define a pagina a ser carregada, adicionando os registros das tabelas 
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # salvar registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            if acao_form == 'Inclusão':
                obj = Categoria(id=None, descricao=form_data['descricao'])
                dao.incluir(obj)

            elif acao_form == 'Exclusão':
                obj = Categoria(id=form_data['id'], descricao=None)
                dao.excluir(obj)

            else:
                obj = Categoria(id=form_data['id'], descricao=form_data['descricao'])
                dao.alterar(obj)

            # Sempre retornar um HttpResponseRedirect após processar dados "POST". 
            # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
            return HttpResponseRedirect( reverse("categorias") )
        
        # inserir registro
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html', {'acao': 'Inclusão'})
        
        # alterar ou excluir
        elif acao in ['alterar', 'excluir']:
            acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
            # seleciona o registro pelo id informado
            obj = dao.selecionar_um(id)
            return render(request, 'categorias_editar.html', {'acao': acao, 'obj': obj})
        
        # acao INVALIDA
        else:
            raise Exception('Ação inválida')

    # se ocorreu algunm erro, insere a mensagem para ser exibida no contexto da página 
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})


def obter_categorias():
    dao = CategoriaDAO()
    return dao.selecionar_todos()


def produtos(request, acao=None, id=None):
    try:
        dao = ProdutoDAO()
        if acao is None:
            registros = dao.selecionar_todos()
            return render(request, 'produtos_listar.html', {'registros': registros})
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data.get('acao')
            categoria = Categoria(id=form_data.get('categoria_id'), descricao=None)
            qtd_estoque = form_data.get('quantidade_estoque') or None

            if acao_form == 'Inclusão':
                produto = Produto(
                    id=None,
                    descricao=form_data.get('descricao'),
                    preco_unitario=form_data.get('preco_unitario'),
                    quantidade_estoque=qtd_estoque,
                    categoria=categoria
                )
                dao.incluir(produto)

            elif acao_form == 'Exclusão':
                produto = Produto(id=form_data.get('id'), descricao=None, preco_unitario=None, quantidade_estoque=None, categoria=None)
                dao.excluir(produto)

            else:
                produto = Produto(
                    id=form_data.get('id'),
                    descricao=form_data.get('descricao'),
                    preco_unitario=form_data.get('preco_unitario'),
                    quantidade_estoque=qtd_estoque,
                    categoria=categoria
                )
                dao.alterar(produto)
            return HttpResponseRedirect(reverse("produtos"))

        elif acao == 'incluir':
            categorias = obter_categorias()
            return render(request, 'produtos_editar.html', {'acao': 'Inclusão', 'categorias': categorias})

        elif acao in ['alterar', 'excluir']:
            obj = dao.selecionar_um(id)
            acao_titulo = 'Alteração' if acao == 'alterar' else 'Exclusão'
            categorias = obter_categorias()
            return render(request, 'produtos_editar.html', {'acao': acao_titulo, 'obj': obj, 'categorias': categorias})

        else:
            raise Exception('Ação inválida para produtos.')

    except Exception as err:
        return render(request, 'home.html', {'ERRO': err})




