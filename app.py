from flask import Flask, render_template, request

app = Flask(__name__)

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

gasolina_aditivada = GasolinaAditivada()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/abastecer', methods=['POST'])
def abastecer():
    tipo = request.form.get('tipo')
    quantidade = request.form.get('quantidade')
    combustivel = request.form.get('combustivel')

    try:
        quantidade = float(quantidade.replace(',', '.'))
    except ValueError:
        return render_template('index.html', resultado="Quantidade inválida. Use números.")

    preco_por_litro = {
        'etanol': 3.50,
        'gasolina': 5.00,
        'diesel': 4.00,
        'gasolina aditivada': 5.80,
        'gnv': 3.00
    }

    if combustivel not in preco_por_litro:
        return render_template('index.html', resultado="Combustível inválido. Por favor, selecione um válido.")

    if tipo == 'litros':
        if combustivel == 'gasolina aditivada':
            resultado = gasolina_aditivada.abastecer_por_litros(quantidade)
        else:
            valor_em_dinheiro = quantidade * preco_por_litro[combustivel]
            resultado = f"Você abasteceu {quantidade:.2f} litros de {combustivel}, que custaram R$ {valor_em_dinheiro:.2f}."
    elif tipo == 'dinheiro':
        if combustivel == 'gasolina aditivada':
            resultado = gasolina_aditivada.abastecer_por_valor(quantidade)
        else:
            litros = quantidade / preco_por_litro[combustivel]
            resultado = f"Você abasteceu R$ {quantidade:.2f}, o que equivale a {litros:.2f} litros de {combustivel}."
    else:
        resultado = "Tipo de abastecimento inválido."

    return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
