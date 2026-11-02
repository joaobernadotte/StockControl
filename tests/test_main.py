from unittest.mock import patch
from src.main import movimentar_estoque



def test_movimentar_estoque_entrada():
    produto = {
        "id": 5,
        "nome": "Teclado Mecânico",
        "quantidade": 10
    }

    with patch(
        "src.main.ler_inteiro",
        side_effect=[5, 20]
    ), patch(
        "src.main.buscar_produto_por_id",
        return_value=produto
    ), patch(
        "builtins.input",
        side_effect=["1", "Compra de mercadorias"]
    ), patch(
        "src.main.registrar_movimentacao_servico",
        return_value=(True, "Movimentação registrada com sucesso!")
    ) as mock_servico:

        movimentar_estoque()

    mock_servico.assert_called_once_with(
        5, "entrada", 20, "Compra de mercadorias"
    )


def test_movimentar_estoque_saida():
    produto = {
        "id": 5,
        "nome": "Teclado Mecânico",
        "quantidade": 30
    }

    with patch(
        "src.main.ler_inteiro",
        side_effect=[5, 8]
    ), patch(
        "src.main.buscar_produto_por_id",
        return_value=produto
    ), patch(
        "builtins.input",
        side_effect=["2", "Venda de mercadorias"]
    ), patch(
        "src.main.registrar_movimentacao_servico",
        return_value=(True, "Movimentação registrada com sucesso!")
    ) as mock_servico:

        movimentar_estoque()

    mock_servico.assert_called_once_with(
        5, "saida", 8, "Venda de mercadorias"
    )


def test_movimentar_estoque_produto_inexistente():
    with patch(
        "src.main.ler_inteiro",
        return_value=999
    ), patch(
        "src.main.buscar_produto_por_id",
        return_value=None
    ), patch(
        "src.main.registrar_movimentacao_servico"
    ) as mock_servico:

        movimentar_estoque()

    mock_servico.assert_not_called()



def test_movimentar_estoque_opcao_invalida():
    produto = {
        "id": 5,
        "nome": "Teclado Mecânico",
        "quantidade": 10
    }

    with patch(
        "src.main.ler_inteiro",
        return_value=5
    ), patch(
        "src.main.buscar_produto_por_id",
        return_value=produto
    ), patch(
        "builtins.input",
        return_value="3"
    ), patch(
        "src.main.registrar_movimentacao_servico"
    ) as mock_servico:

        movimentar_estoque()

    mock_servico.assert_not_called()


def test_movimentar_estoque_quantidade_zero():
    produto = {
        "id": 5,
        "nome": "Teclado Mecânico",
        "quantidade": 10
    }

    with patch(
        "src.main.ler_inteiro",
        side_effect=[5, 0]
    ), patch(
        "src.main.buscar_produto_por_id",
        return_value=produto
    ), patch(
        "builtins.input",
        side_effect=["1"]
    ), patch(
        "src.main.registrar_movimentacao_servico"
    ) as mock_servico:

        movimentar_estoque()

    mock_servico.assert_not_called()
