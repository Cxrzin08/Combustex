class Gasolina:
    def __init__(self):
        self.preco_por_litro = 5.20
        self.quantidade_disponivel = 4000

    def abastecer_por_litros(self, litros):
        if litros > self.quantidade_disponivel:
            return "Quantidade de gasolina comum indisponível para abastecimento."
        custo = litros * self.preco_por_litro
        self.quantidade_disponivel -= litros
        return f"Abastecido com {litros} litros de gasolina comum. Total a pagar: R${custo:.2f}"

    def abastecer_por_valor(self, valor):
        litros = valor / self.preco_por_litro
        if litros > self.quantidade_disponivel:
            return "Quantidade de gasolina comum indisponível para abastecimento."
        self.quantidade_disponivel -= litros
        return f"Abastecido com R${valor:.2f} de gasolina comum. Total de litros: {litros:.2f}L"
