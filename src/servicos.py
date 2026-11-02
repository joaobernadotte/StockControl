
from src.database import (
    cadastrar_produto,
    atualizar_produto,
    excluir_produto
)

def validar_dados_produto(
    nome,
    preco_compra,
    preco_venda,
    quantidade,
    estoque_minimo
):
    if not nome.strip():
        return False, "O nome do produto é obrigatório."

    if preco_compra < 0:
        return False, "O preço de compra não pode ser negativo."

    if preco_venda <= 0:
        return False, "O preço de venda precisa ser maior que zero."

    if quantidade < 0:
        return False, "A quantidade não pode ser negativa."

    if estoque_minimo < 0:
        return False, "O estoque mínimo não pode ser negativo."

    return True, "Dados válidos."


def validar_atualizacao_produto(campo, novo_valor):
    campos_texto = {
        "1": "nome",
        "2": "descricao"
    }

    campos_numericos = {
        "3": "preco_compra",
        "4": "preco_venda",
        "5": "quantidade",
        "6": "estoque_minimo"
    }

    if campo not in campos_texto and campo not in campos_numericos:
        return False, "Campo inválido."

    if campo == "1" and not novo_valor.strip():
        return False, "O nome do produto é obrigatório."

    if campo in ("3", "5", "6") and novo_valor < 0:
        return False, "O valor não pode ser negativo."

    if campo == "4" and novo_valor <= 0:
        return False, "O preço de venda precisa ser maior que zero."

    return True, "Atualização válida."



def cadastrar_produto_servico(
    nome, descricao, preco_compra, preco_venda, quantidade, estoque_minimo
):
    valido, mensagem = validar_dados_produto(
        nome,
        preco_compra,
        preco_venda,
        quantidade,
        estoque_minimo
    )

    if not valido:
        return False, mensagem

    return cadastrar_produto(
        nome,
        descricao,
        preco_compra,
        preco_venda,
        quantidade,
        estoque_minimo
    )




def atualizar_produto_servico(id_produto, campo, novo_valor):
    valido, mensagem = validar_atualizacao_produto(
        campo,
        novo_valor
    )

    if not valido:
        return False, mensagem

    return atualizar_produto(
        id_produto,
        campo,
        novo_valor
    )

def excluir_produto_servico(id_produto):
    return excluir_produto(id_produto)
