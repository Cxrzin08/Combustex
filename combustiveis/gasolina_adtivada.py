class GasolinaAditivada:
    def __init__(self):
        self.preco_por_litro = 5.80
        self.quantidade_disponivel = 3000

    def abastecer_por_litros(self, litros):
        if litros > self.quantidade_disponivel:
            return "Quantidade de gasolina aditivada indisponível para abastecimento."
        custo = litros * self.preco_por_litro
        self.quantidade_disponivel -= litros
        return f"Você abasteceu {litros:.2f} litros de gasolina aditivada, que custaram R$ {custo:.2f}."

    def abastecer_por_valor(self, valor):
        litros = valor / self.preco_por_litro
        if litros > self.quantidade_disponivel:
            return "Quantidade de gasolina aditivada indisponível para abastecimento."
        self.quantidade_disponivel -= litros
        return f"Você abasteceu R$ {valor:.2f} de gasolina aditivada, que equivale a {litros:.2f} litros."
