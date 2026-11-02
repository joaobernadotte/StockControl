
from unittest.mock import patch

from src.servicos import (
    validar_dados_produto,
    validar_atualizacao_produto,
    cadastrar_produto_servico,
    atualizar_produto_servico,
    registrar_movimentacao_servico
)

def test_dados_produto_validos():
    resultado, mensagem = validar_dados_produto(
        "Teclado Mecânico",
        150.00,
        250.00,
        10,
        3
    )

    assert resultado is True
    assert mensagem == "Dados válidos."


def test_nome_produto_vazio():
    resultado, mensagem = validar_dados_produto(
        "   ",
        150.00,
        250.00,
        10,
        3
    )

    assert resultado is False
    assert mensagem == "O nome do produto é obrigatório."


def test_preco_compra_negativo():
    resultado, mensagem = validar_dados_produto(
        "Teclado",
        -10,
        250,
        10,
        3
    )

    assert resultado is False
    assert mensagem == "O preço de compra não pode ser negativo."


def test_preco_venda_zero():
    resultado, mensagem = validar_dados_produto(
        "Teclado",
        150,
        0,
        10,
        3
    )

    assert resultado is False
    assert mensagem == "O preço de venda precisa ser maior que zero."


def test_quantidade_negativa():
    resultado, mensagem = validar_dados_produto(
        "Teclado",
        150,
        250,
        -1,
        3
    )

    assert resultado is False
    assert mensagem == "A quantidade não pode ser negativa."


def test_estoque_minimo_negativo():
    resultado, mensagem = validar_dados_produto(
        "Teclado",
        150,
        250,
        10,
        -1
    )

    assert resultado is False
    assert mensagem == "O estoque mínimo não pode ser negativo."

def test_atualizacao_com_preco_venda_valido():
    resultado, mensagem = validar_atualizacao_produto("4", 250.00)

    assert resultado is True
    assert mensagem == "Atualização válida."


def test_atualizacao_com_preco_venda_zero():
    resultado, mensagem = validar_atualizacao_produto("4", 0)

    assert resultado is False
    assert mensagem == "O preço de venda precisa ser maior que zero."


def test_atualizacao_com_nome_vazio():
    resultado, mensagem = validar_atualizacao_produto("1", "   ")

    assert resultado is False
    assert mensagem == "O nome do produto é obrigatório."



def test_atualizacao_com_quantidade_negativa():
    resultado, mensagem = validar_atualizacao_produto("5", -10)

    assert resultado is False
    assert "não pode ser alterada diretamente" in mensagem
    assert "movimentações" in mensagem



def test_atualizacao_com_campo_invalido():
    resultado, mensagem = validar_atualizacao_produto("9", 100)

    assert resultado is False
    assert mensagem == "Campo inválido."




def test_cadastrar_produto_servico_com_dados_validos():
    with patch(
        "src.servicos.cadastrar_produto",
        return_value=(True, "Produto cadastrado com sucesso!")
    ) as cadastro:
        resultado, mensagem = cadastrar_produto_servico(
            "Teclado",
            "Teclado mecânico",
            150,
            250,
            10,
            3
        )

    assert resultado is True
    assert mensagem == "Produto cadastrado com sucesso!"

    cadastro.assert_called_once_with(
        "Teclado",
        "Teclado mecânico",
        150,
        250,
        10,
        3
    )


def test_cadastrar_produto_servico_com_nome_vazio():
    with patch("src.servicos.cadastrar_produto") as cadastro:
        resultado, mensagem = cadastrar_produto_servico(
            "   ",
            "Teclado mecânico",
            150,
            250,
            10,
            3
        )

    assert resultado is False
    assert mensagem == "O nome do produto é obrigatório."
    cadastro.assert_not_called()


def test_atualizar_produto_servico_com_dados_validos():
    with patch(
        "src.servicos.atualizar_produto",
        return_value=(True, "Produto atualizado com sucesso!")
    ) as atualizacao:

        resultado, mensagem = atualizar_produto_servico(
            1,
            "4",
            299.90
        )

    assert resultado is True
    assert mensagem == "Produto atualizado com sucesso!"

    atualizacao.assert_called_once_with(
        1,
        "4",
        299.90
    )


def test_atualizar_produto_servico_com_preco_invalido():
    with patch("src.servicos.atualizar_produto") as atualizacao:
        resultado, mensagem = atualizar_produto_servico(
            1,
            "4",
            0
        )

    assert resultado is False
    assert mensagem == "O preço de venda precisa ser maior que zero."
    atualizacao.assert_not_called()


def test_cadastrar_produto_servico_com_falha_no_banco():
    with patch(
        "src.servicos.cadastrar_produto",
        return_value=(False, "Erro ao cadastrar produto: Falha na conexão")
    ) as cadastro:
        resultado, mensagem = cadastrar_produto_servico(
            "Teclado",
            "Teclado mecânico",
            150,
            250,
            10,
            3
        )

    assert resultado is False
    assert mensagem == "Erro ao cadastrar produto: Falha na conexão"

    cadastro.assert_called_once()


def test_validar_atualizacao_produto_rejeita_alteracao_quantidade():
    valido, mensagem = validar_atualizacao_produto("5", 20)

    assert valido is False
    assert "não pode ser alterada diretamente" in mensagem
    assert "movimentações" in mensagem


def test_registrar_movimentacao_servico_com_dados_validos():
    with patch(
        "src.servicos.registrar_movimentacao",
        return_value=(True, "Movimentação registrada com sucesso!")
    ) as mock_movimentacao:

        sucesso, mensagem = registrar_movimentacao_servico(
            5, "entrada", 20, "Compra"
        )

    assert sucesso is True
    assert mensagem == "Movimentação registrada com sucesso!"

    mock_movimentacao.assert_called_once_with(
        5, "entrada", 20, "Compra"
    )


def test_registrar_movimentacao_servico_com_tipo_invalido():
    with patch("src.servicos.registrar_movimentacao") as mock_movimentacao:
        sucesso, mensagem = registrar_movimentacao_servico(
            5, "transferencia", 10, "Teste"
        )

    assert sucesso is False
    assert mensagem == "Tipo de movimentação inválido."

    mock_movimentacao.assert_not_called()


def test_registrar_movimentacao_servico_com_quantidade_invalida():
    with patch("src.servicos.registrar_movimentacao") as mock_movimentacao:
        sucesso, mensagem = registrar_movimentacao_servico(
            5, "entrada", 0, "Teste"
        )

    assert sucesso is False
    assert mensagem == "A quantidade deve ser maior que zero."

    mock_movimentacao.assert_not_called()
