import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar():
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

    return conexao

def testar_conexao():
    conexao = None
    try:
        conexao = conectar()
        if conexao.is_connected():
            print("Conexão com o MySQL estabelecida com sucesso!")

    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão encerrada.")

def listar_produtos():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT
                id,
                nome,
                preco_venda,
                quantidade
            FROM produtos
            ORDER BY id ASC
        """

        cursor.execute(sql)
        produtos = cursor.fetchall()

        return produtos

    except mysql.connector.Error as erro:
        print(f"Erro ao listar produtos: {erro}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()


def cadastrar_produto(
    nome, descricao, preco_compra, preco_venda, quantidade, estoque_minimo
):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO produtos
            (nome, descricao, preco_compra, preco_venda, quantidade, estoque_minimo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome,
            descricao,
            preco_compra,
            preco_venda,
            quantidade,
            estoque_minimo
        )

        cursor.execute(sql, valores)
        conexao.commit()

        return True, "Produto cadastrado com sucesso!"

    except mysql.connector.Error as erro:
        if conexao is not None:
            conexao.rollback()

        return False, f"Erro ao cadastrar produto: {erro}"

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()





def atualizar_produto(id_produto, campo, novo_valor):
    conexao = None
    cursor = None

    campos_permitidos = {
        "1": "nome",
        "2": "descricao",
        "3": "preco_compra",
        "4": "preco_venda",
        "6": "estoque_minimo"
    }

    if campo not in campos_permitidos:
        return False, "Campo inválido."

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        nome_coluna = campos_permitidos[campo]

        sql = f"""
            UPDATE produtos
            SET {nome_coluna} = %s
            WHERE id = %s
        """

        valores = (novo_valor, id_produto)

        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount == 0:
            return False, "Produto não encontrado ou nenhum dado foi alterado."

        return True, "Produto atualizado com sucesso!"

    except mysql.connector.Error as erro:
        if conexao is not None:
            conexao.rollback()

        return False, f"Erro ao atualizar produto: {erro}"

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()


def excluir_produto(id_produto):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = "DELETE FROM produtos WHERE id = %s"

        cursor.execute(sql, (id_produto,))
        conexao.commit()

        if cursor.rowcount > 0:
            return True, "Produto excluído com sucesso!"

        return False, "Produto não encontrado."

    except mysql.connector.IntegrityError:
        if conexao is not None:
            conexao.rollback()

        return False, (
            "Não é possível excluir este produto, "
            "pois ele possui movimentações registradas."
        )

    except mysql.connector.Error as erro:
        if conexao is not None:
            conexao.rollback()

        return False, f"Erro ao excluir produto: {erro}"

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()


def buscar_produto_por_id(id_produto):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM produtos
            WHERE id = %s
        """

        cursor.execute(sql, (id_produto,))
        produto = cursor.fetchone()

        return produto

    except mysql.connector.Error as erro:
        print(f"Erro ao buscar produto: {erro}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()

def listar_produtos_estoque_baixo():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT
                id,
                nome,
                quantidade,
                estoque_minimo
            FROM produtos
            WHERE quantidade <= estoque_minimo
            ORDER BY quantidade ASC
        """

        cursor.execute(sql)
        produtos = cursor.fetchall()

        return produtos

    except mysql.connector.Error as erro:
        print(f"Erro ao consultar estoque: {erro}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()


def registrar_movimentacao(
    id_produto, tipo, quantidade, observacao
):
    conexao = None
    cursor = None

    try:
        # Validar os dados básicos
        if tipo not in ("entrada", "saida"):
            return False, "Tipo de movimentação inválido."

        if quantidade <= 0:
            return False, "A quantidade deve ser maior que zero."

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        # Consultar e bloquear o produto durante a transação
        sql_buscar = """
            SELECT id, quantidade
            FROM produtos
            WHERE id = %s
            FOR UPDATE
        """

        cursor.execute(sql_buscar, (id_produto,))
        produto = cursor.fetchone()

        if produto is None:
            conexao.rollback()
            return False, "Produto não encontrado."

        estoque_atual = produto["quantidade"]

        # Calcular o novo estoque
        if tipo == "entrada":
            novo_estoque = estoque_atual + quantidade
        else:
            if quantidade > estoque_atual:
                conexao.rollback()
                return False, "Estoque insuficiente."

            novo_estoque = estoque_atual - quantidade

        # Atualizar o estoque
        sql_atualizar = """
            UPDATE produtos
            SET quantidade = %s
            WHERE id = %s
        """

        cursor.execute(
            sql_atualizar,
            (novo_estoque, id_produto)
        )

        # Registrar a movimentação
        sql_movimentacao = """
            INSERT INTO movimentacoes
            (produto_id, tipo, quantidade, observacao)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql_movimentacao,
            (id_produto, tipo, quantidade, observacao)
        )

        conexao.commit()

        return True, "Movimentação registrada com sucesso!"

    except mysql.connector.Error as erro:
        if conexao is not None:
            conexao.rollback()

        return False, f"Erro ao registrar movimentação: {erro}"

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()

