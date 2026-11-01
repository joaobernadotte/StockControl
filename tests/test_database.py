import mysql.connector

from unittest.mock import MagicMock, patch
from src.database import (
    buscar_produto_por_id,
    cadastrar_produto,
    atualizar_produto,
    excluir_produto,
    listar_produtos_estoque_baixo
)


def test_buscar_produto_por_id():
    produto_esperado = {
        "id": 1,
        "nome": "Teclado Mecânico",
        "preco_venda": 250.00,
        "quantidade": 15
    }

    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso
    conexao_falsa.is_connected.return_value = True

    cursor_falso.fetchone.return_value = produto_esperado

    with patch(
        "src.database.conectar",
        return_value=conexao_falsa
    ):
        resultado = buscar_produto_por_id(1)

    assert resultado == produto_esperado

    cursor_falso.execute.assert_called_once_with(
        """
            SELECT *
            FROM produtos
            WHERE id = %s
        """,
        (1,)
    )

    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()



def test_cadastrar_produto():
    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso
    conexao_falsa.is_connected.return_value = True

    with patch(
        "src.database.conectar",
        return_value=conexao_falsa
    ):
        resultado = cadastrar_produto(
            "Webcam HD",
            "Webcam USB 1080p",
            100.00,
            159.90,
            12,
            3
        )

    assert resultado == (True, "Produto cadastrado com sucesso!")

    cursor_falso.execute.assert_called_once_with(
        """
            INSERT INTO produtos
            (nome, descricao, preco_compra, preco_venda, quantidade, estoque_minimo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            "Webcam HD",
            "Webcam USB 1080p",
            100.00,
            159.90,
            12,
            3
        )
    )

    conexao_falsa.commit.assert_called_once()
    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()


def test_atualizar_produto():
    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso
    conexao_falsa.is_connected.return_value = True
    cursor_falso.rowcount = 1

    with patch(
        "src.database.conectar",
        return_value=conexao_falsa
    ):
        atualizar_produto(1, "5", 25)

    cursor_falso.execute.assert_called_once_with(
        "UPDATE produtos SET quantidade = %s WHERE id = %s",
        (25, 1)
    )

    conexao_falsa.commit.assert_called_once()
    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()

def test_excluir_produto():
    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso
    conexao_falsa.is_connected.return_value = True

    cursor_falso.rowcount = 1

    with patch(
        "src.database.conectar",
        return_value=conexao_falsa
    ):
        excluir_produto(5)

    cursor_falso.execute.assert_called_once_with(
        "DELETE FROM produtos WHERE id = %s",
        (5,)
    )

    conexao_falsa.commit.assert_called_once()
    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()

def test_atualizar_produto_sem_registro_afetado(capsys):
    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso
    conexao_falsa.is_connected.return_value = True

    cursor_falso.rowcount = 0

    with patch(
        "src.database.conectar",
        return_value=conexao_falsa
    ):
        atualizar_produto(9999, "5", 25)

    captura = capsys.readouterr()

    assert "Produto não encontrado ou nenhum dado foi alterado." in captura.out

    conexao_falsa.commit.assert_called_once()
    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()

def test_buscar_produto_inexistente():
    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso
    conexao_falsa.is_connected.return_value = True

    cursor_falso.fetchone.return_value = None

    with patch(
        "src.database.conectar",
        return_value=conexao_falsa
    ):
        resultado = buscar_produto_por_id(9999)

    assert resultado is None

    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()


def test_listar_produtos_estoque_baixo():
    conexao_falsa = MagicMock()
    cursor_falso = MagicMock()

    conexao_falsa.cursor.return_value = cursor_falso

    produtos_falsos = [
        {
            "id": 1,
            "nome": "Teclado Mecânico",
            "quantidade": 2,
            "estoque_minimo": 5
        }
    ]

    cursor_falso.fetchall.return_value = produtos_falsos

    with patch("src.database.conectar", return_value=conexao_falsa):
        resultado = listar_produtos_estoque_baixo()

    assert resultado == produtos_falsos

    cursor_falso.execute.assert_called_once()
    cursor_falso.close.assert_called_once()
    conexao_falsa.close.assert_called_once()



def test_falha_na_conexao_ao_cadastrar_produto():
    with patch(
        "src.database.conectar",
        side_effect=mysql.connector.Error("Falha na conexão")
    ):
        resultado = cadastrar_produto(
            "Mouse",
            "Mouse sem fio",
            50.00,
            90.00,
            10,
            2
        )

    assert resultado[0] is False
    assert "Erro ao cadastrar produto" in resultado[1]
    assert "Falha na conexão" in resultado[1]



