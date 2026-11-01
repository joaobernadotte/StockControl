def ler_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))

            if valor < 0:
                print("Digite um número igual ou maior que zero.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")


def ler_decimal(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))

            if valor < 0:
                print("Digite um valor igual ou maior que zero.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida! Digite um número válido.")