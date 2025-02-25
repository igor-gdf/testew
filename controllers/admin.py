from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Jogo import Jogo
from utils import db
from functools import wraps
from flask_login import current_user, login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Usando current_user para verificar a função do usuário
        if current_user.funcao != 'admin':
            flash('Acesso restrito: somente administradores podem acessar esta página.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/jogos_pendentes')
@admin_required
@login_required  # Garantindo que o usuário está logado antes de acessar a página
def jogos_pendentes():
    jogos = Jogo.query.all()  
    return render_template('jogos_pendentes.html', jogos=jogos)

@admin_bp.route('/validar_jogos/<int:jogo_id>', methods=['GET', 'POST'])
@admin_required
@login_required  # Garantindo que o usuário está logado antes de acessar a página
def validar_jogos(jogo_id):
    jogo = Jogo.query.get_or_404(jogo_id)
    
    if current_user is None:  # Verificando se o usuário está logado
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        novo_status = request.form.get('status')
        if novo_status not in ["aprovado", "reprovado", "pendente"]:
            flash("Status inválido!", "danger")
            return redirect(url_for('admin.validar_jogos', jogo_id=jogo_id))
        
        jogo.status = novo_status
        db.session.commit()
        flash("Jogo atualizado com sucesso!", "success")
        return redirect(url_for('admin.jogos_pendentes'))
    
    return render_template('validar_jogos.html', jogo=jogo)
