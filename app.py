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
from datetime import timedelta

# Inicializando a aplicação Flask
app = Flask(__name__)

# Registrando blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(dev_bp)

# Configurações do banco de dados e chave secreta
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'uma_chave_secreta_unica_e_complexa')  # Defina uma chave secreta para a sessão
app.config['DEBUG'] = False  # Desabilita o modo debug em produção
app.permanent_session_lifetime = timedelta(minutes=30)  # Define o tempo de expiração da sessão

# Inicializando banco de dados e migrações
db.init_app(app)
migrate = Migrate(app, db)

# Inicializando o login_manager do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Função de carregamento de usuário
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Definindo o modelo User para o Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Rota de cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        funcao = request.form['funcao']

        # Verificando se o email já está cadastrado
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))

        # Criptografando a senha antes de salvar
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash, funcao=funcao)

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

        # Verificando o usuário e senha
        usuario_obj = Usuario.query.filter_by(nome=usuario).first()
        
        if usuario_obj and usuario_obj.verificar_senha(senha):  # A senha será verificada com senha_hash
            login_user(usuario_obj)  # Flask-Login gerencia a sessão
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota do dashboard (apenas para usuários logados)
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

# Outras rotas
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

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi deslogado com sucesso.', 'success')
    return redirect(url_for('login'))

# Rota de jogo
@app.route('/jogos')
@login_required
def jogos():
    # Buscando todos os jogos com status 'validado'
    jogos_validos = Jogo.query.filter_by(status="validado").all()
    return render_template('jogos.html', jogos=jogos_validos)

@app.route('/jogo/<int:jogo_id>')
@login_required
def jogo_detalhes(jogo_id):
    jogo = Jogo.query.get_or_404(jogo_id)
    return render_template('jogo_detalhes.html', jogo=jogo)


# Rodando a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas do banco de dados se não existirem
    app.run(debug=True)
