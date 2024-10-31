from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import pickle
import os

app = Flask(__name__)
app.secret_key = 'Combustex_posto'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

USUARIOS_FILE = 'usuarios.pkl'

def load_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'rb') as file:
            return pickle.load(file)
    return {}

def save_usuarios(usuarios):
    with open(USUARIOS_FILE, 'wb') as file:
        pickle.dump(usuarios, file)

usuarios = load_usuarios()

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

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario in usuarios:
            return render_template('cadastro.html', erro="Usuário já existe. Tente outro nome de usuário.")

        usuarios[usuario] = senha
        save_usuarios(usuarios)
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuarios.get(usuario) == senha:
            session['usuario'] = usuario
            return redirect(url_for('menucombustivel'))  # Redireciona para o menu de combustíveis
        else:
            return render_template('login.html', erro="Credenciais inválidas. Tente novamente.")
    return render_template('login.html')

@app.route('/esqueceu_senha', methods=['GET', 'POST'])
def esqueceu_senha():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        nova_senha = request.form.get('nova_senha')

        if usuario in usuarios:
            usuarios[usuario] = nova_senha
            save_usuarios(usuarios)
            return redirect(url_for('login'))
        else:
            return render_template('esqueceu_senha.html', erro="Usuário não encontrado.")
    return render_template('esqueceu_senha.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menucombustivel')
def menucombustivel():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('menucombustivel.html')  # Renderiza a página de menu de combustíveis

@app.route('/abastecer', methods=['POST'])
def abastecer():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    tipo = request.form.get('tipo')
    quantidade = request.form.get('quantidade')
    combustivel = request.form.get('combustivel')

    try:
        quantidade = float(quantidade.replace(',', '.'))
    except ValueError:
        return render_template('menucombustivel.html', resultado="Quantidade inválida. Use números.")

    preco_por_litro = {
        'etanol': 3.50,
        'gasolina': 5.00,
        'diesel': 4.00,
        'gasolina aditivada': 5.80,
        'gnv': 3.00
    }

    if combustivel not in preco_por_litro:
        return render_template('menucombustivel.html', resultado="Combustível inválido. Por favor, selecione um válido.")

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

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
