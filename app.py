from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import db
import os
from flask_migrate import Migrate
from models.Usuario import Usuario
from controllers.Usuario import bp_usuarios

app = Flask(__name__)
#app.register_blueprint(bp_usuarios, url_prefix='/usuarios')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#db_host = os.getenv('DB_HOST')
#db_usuario = os.getenv('DB_USERNAME')
#db_senha = os.getenv('DB_PASSWORD')
#db_mydb = os.getenv('DB_DATABASE')

#conexao = f"mysql+pymysql://{db_usuario}:{db_senha}@{db_host}/{db_mydb}"
#app.config['SQLALCHEMY_DATABASE_URI'] = conexao
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Usuarios exemplo
USERS = {
    'user@example.com': 'senha123'
}

jogos_mais_jogados = [
    {'nome': 'Jogo A', 'jogadores': 5000},
    {'nome': 'Jogo B', 'jogadores': 3500},
]

jogos_recentes = [
    {'nome': 'Jogo X', 'data_adicao': '2024-08-10'},
    {'nome': 'Jogo Y', 'data_adicao': '2024-08-15'},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        funcao = request.form['funcao']

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario = Usuario(nome=nome, email=email, senha=senha, funcao=funcao)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar usuário: {e}', 'danger')

    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        if USERS.get(email) == senha:
            session['usuario'] = email
            return redirect(url_for('home'))
        else:
            flash('E-mail ou senha incorretos. Tente novamente.')
            return redirect(url_for('login'))
    
    return render_template('home.html', jogos_mais_jogados=jogos_mais_jogados, jogos_recentes=jogos_recentes)

@app.route('/beneficios')
def beneficios():
    return render_template('beneficios.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/perfil', defaults={"nome": "usuario_demo"})
@app.route('/perfil/<nome>')
def perfil(nome):
    return render_template('perfil.html', nome=nome)

@app.route('/projetos')
def projetos():
    return render_template('projetos.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Você foi deslogado com sucesso.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)