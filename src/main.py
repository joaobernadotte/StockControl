
from src.database import (
    listar_produtos,
    excluir_produto,
    buscar_produto_por_id,
    listar_produtos_estoque_baixo
)

from src.servicos import (
    cadastrar_produto_servico,
    atualizar_produto_servico,
    excluir_produto_servico,
    registrar_movimentacao_servico
)

from src.validacoes import ler_inteiro, ler_decimal


def exibir_menu():
    print("\n===== STOCK CONTROL =====")
    print("1 - Listar produtos")
    print("2 - Cadastrar produto")
    print("3 - Atualizar produto")
    print("4 - Excluir produto")
    print("5 - Sair")
    print("6 - Relatório de estoque baixo")
    print("7 - Movimentar estoque")


def listar():
    produtos = listar_produtos()

    if produtos is None:
        print("Não foi possível listar os produtos.")
        return

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("\n===== PRODUTOS CADASTRADOS =====")

    for produto in produtos:
        print(f"\nID: {produto['id']}")
        print(f"Nome: {produto['nome']}")
        print(f"Preço de venda: R$ {produto['preco_venda']}")
        print(f"Quantidade: {produto['quantidade']}")


def cadastrar():
    print("\n===== CADASTRAR PRODUTO =====")

    nome = input("Nome do produto: ").strip()
    descricao = input("Descrição: ").strip()
    preco_compra = ler_decimal("Preço de compra: ")
    preco_venda = ler_decimal("Preço de venda: ")
    quantidade = ler_inteiro("Quantidade: ")
    estoque_minimo = ler_inteiro("Estoque mínimo: ")

    sucesso, mensagem = cadastrar_produto_servico(
        nome,
        descricao,
        preco_compra,
        preco_venda,
        quantidade,
        estoque_minimo
    )

    print(mensagem)


def atualizar():
    print("\n===== ATUALIZAR PRODUTO =====")

    id_produto = ler_inteiro("Digite o ID do produto: ")

    produto = buscar_produto_por_id(id_produto)

    if produto is None:
        print("Produto não encontrado ou não foi possível consultar o banco.")
        return

    print("\nProduto encontrado:")
    print(f"Nome: {produto['nome']}")
    print(f"Preço de compra: R$ {produto['preco_compra']}")
    print(f"Preço de venda: R$ {produto['preco_venda']}")
    print(f"Quantidade: {produto['quantidade']}")

    print("\nQual informação deseja atualizar?")
    print("1 - Nome")
    print("2 - Descrição")
    print("3 - Preço de compra")
    print("4 - Preço de venda")
    print("6 - Estoque mínimo")

    campo = input("Escolha uma opção: ").strip()

    if campo == "1":
        novo_valor = input("Novo nome: ").strip()

    elif campo == "2":
        novo_valor = input("Nova descrição: ").strip()

    elif campo in ("3", "4"):
        novo_valor = ler_decimal("Novo valor: ")

    elif campo in "6":
        novo_valor = ler_inteiro("Novo valor: ")

    else:
        print("Opção inválida.")
        return

    sucesso, mensagem = atualizar_produto_servico(
        id_produto,
        campo,
        novo_valor
    )

    print(mensagem)


def movimentar_estoque():
    print("\n===== MOVIMENTAÇÃO DE ESTOQUE =====")

    id_produto = ler_inteiro("Digite o ID do produto: ")

    produto = buscar_produto_por_id(id_produto)

    if produto is None:
        print("Produto não encontrado ou não foi possível consultar o banco.")
        return

    print(f"\nProduto: {produto['nome']}")
    print(f"Estoque atual: {produto['quantidade']} unidades")

    print("\nTipos de movimentação:")
    print("1 - Entrada")
    print("2 - Saída")

    tipo_opcao = input("Escolha uma opção: ").strip()

    if tipo_opcao == "1":
        tipo = "entrada"
    elif tipo_opcao == "2":
        tipo = "saida"
    else:
        print("Opção inválida.")
        return

    quantidade = ler_inteiro("Digite a quantidade: ")

    if quantidade == 0:
        print("A quantidade deve ser maior que zero.")
        return

    observacao = input("Digite uma observação: ").strip()

    sucesso, mensagem = registrar_movimentacao_servico(
        id_produto,
        tipo,
        quantidade,
        observacao
    )

    print(f"\n{mensagem}")


def excluir():
    print("\n===== EXCLUIR PRODUTO =====")

    id_produto = ler_inteiro("Digite o ID do produto: ")

    produto = buscar_produto_por_id(id_produto)

    if produto is None:
        print("Produto não encontrado ou não foi possível consultar o banco.")
        return

    print(f"\nProduto: {produto['nome']}")

    confirmacao = input(
        "Tem certeza que deseja excluir este produto? (s/n): "
    ).strip().lower()

    if confirmacao == "s":
        sucesso, mensagem = excluir_produto_servico(id_produto)
        print(mensagem)
    else:
        print("Exclusão cancelada.")


def relatorio_estoque_baixo():
    print("\n===== RELATÓRIO DE ESTOQUE BAIXO =====")

    produtos = listar_produtos_estoque_baixo()

    if produtos is None:
        print("Não foi possível consultar o estoque.")
        return

    if not produtos:
        print("Nenhum produto com estoque baixo.")
        return

    for produto in produtos:
        print(f"\nID: {produto['id']}")
        print(f"Nome: {produto['nome']}")
        print(f"Quantidade atual: {produto['quantidade']}")
        print(f"Estoque mínimo: {produto['estoque_minimo']}")


def main():
    while True:
        exibir_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            listar()

        elif opcao == "2":
            cadastrar()

        elif opcao == "3":
            atualizar()

        elif opcao == "4":
            excluir()

        elif opcao == "5":
            print("Encerrando o StockControl. Até mais!")
            break

        elif opcao == "6":
            relatorio_estoque_baixo()

        elif opcao == "7":
            movimentar_estoque()

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
