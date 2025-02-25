from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Jogo import Jogo
from utils import db
from functools import wraps
from flask_login import login_required, current_user

dev_bp = Blueprint('dev', __name__, url_prefix='/dashboard')

def developer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificando a função do usuário com current_user
        if current_user.funcao != 'desenvolvedor':
            flash('Acesso restrito: somente desenvolvedores podem enviar jogos.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@dev_bp.route('/criar_jogos', methods=['GET', 'POST'])
@login_required
@developer_required
def criar_jogos():
    if current_user is None:  # Verificando se o usuário está logado
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        url_download = request.form.get('url_download')

        if not titulo or not descricao or not url_download:
            flash("Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for('dev.criar_jogos'))
        
        id_usuario = current_user.id  # Usando current_user.id para pegar o ID do usuário
        
        if not id_usuario:
            flash("Usuário não autenticado corretamente.", "danger")
            return redirect(url_for('login'))

        jogo = Jogo(
            id_criador=id_usuario,
            titulo=titulo,
            descricao=descricao,
            url_download=url_download,
            status="pendente"
        )
        jogo.id_desenvolvedor = id_usuario
        
        db.session.add(jogo)
        db.session.commit()

        flash("Jogo enviado com sucesso! Aguarde a validação do administrador.", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('criar_jogos.html')
