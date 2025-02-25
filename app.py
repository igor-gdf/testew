from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import db
import os
from flask_migrate import Migrate
from models.Usuario import Usuario
from models.Jogo import Jogo
from models.Jogar import Jogar
from models.Categoria import Categoria
from controllers.Usuario import bp_usuarios
from controllers.admin import admin_bp
from controllers.desenvolvedor import dev_bp
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.register_blueprint(admin_bp)
app.register_blueprint(dev_bp)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

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
            flash('Usuário cadastrado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar usuário: {e}', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        usuario_obj = Usuario.query.filter_by(nome=usuario).first()
        
        if usuario_obj and usuario_obj.verificar_senha(senha):
            login_user(usuario_obj)  # Flask-Login gerencia a sessão
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

from flask_login import login_required

@app.route('/dashboard')
@login_required
def dashboard():
    jogos_mais_jogados = [
        {'nome': 'Jogo A', 'jogadores': 5000},
        {'nome': 'Jogo B', 'jogadores': 3500},
    ]

    jogos_recentes = [
        {'nome': 'Jogo X', 'data_adicao': '2024-08-10'},
        {'nome': 'Jogo Y', 'data_adicao': '2024-08-15'},
    ]

    return render_template('dashboard.html', jogos_mais_jogados=jogos_mais_jogados, jogos_recentes=jogos_recentes)



@app.route('/beneficios')
def beneficios():
    return render_template('beneficios.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/perfil', defaults={"nome": "usuario_demo"})
@app.route('/perfil/<nome>')
@login_required
def perfil(nome):
    return render_template('perfil.html', nome=nome)

@app.route('/projetos')
def projetos():
    return render_template('projetos.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado com sucesso.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
