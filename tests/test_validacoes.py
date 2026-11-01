from src.validacoes import ler_inteiro, ler_decimal


def test_ler_inteiro_valido(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda mensagem: "10")

    resultado = ler_inteiro("Digite um número: ")

    assert resultado == 10


def test_ler_inteiro_rejeita_valor_negativo(monkeypatch):
    entradas = iter(["-5", "10"])
    monkeypatch.setattr("builtins.input", lambda mensagem: next(entradas))

    resultado = ler_inteiro("Digite um número: ")

    assert resultado == 10


def test_ler_decimal_aceita_virgula(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda mensagem: "50,90")

    resultado = ler_decimal("Digite um preço: ")

    assert resultado == 50.90

def test_ler_inteiro_rejeita_texto(monkeypatch):
    entradas = iter(["abc", "15"])
    monkeypatch.setattr("builtins.input", lambda mensagem: next(entradas))

    resultado = ler_inteiro("Digite um número: ")

    assert resultado == 15


def test_ler_decimal_rejeita_valor_negativo(monkeypatch):
    entradas = iter(["-20", "35.50"])
    monkeypatch.setattr("builtins.input", lambda mensagem: next(entradas))

    resultado = ler_decimal("Digite um preço: ")

    assert resultado == 35.50