from flask import render_template, request, redirect, flash, url_for
from models.Usuario import Usuario
from utils import db
from flask import Blueprint

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('usuarios_create.html')
    
    elif request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        funcao = request.form['funcao']  

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('.create'))
        
        usuario = Usuario(nome=nome, email=email, senha=senha, funcao=funcao)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('.recovery'))


@bp_usuarios.route('/recovery', defaults={'id': 0})
@bp_usuarios.route('/recovery/<int:id>')
def recovery(id):
    if id == 0:
        usuarios = Usuario.query.all()
        return render_template('usuarios_recovery.html', usuarios=usuarios)
    else:
        usuario = Usuario.query.get(id)
        if not usuario:
            flash('Usuário não encontrado!', 'danger')
            return redirect(url_for('.recovery'))
        return render_template('usuarios_detalhes.html', usuario=usuario)


@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('.recovery'))

    if request.method == 'GET':
        return render_template('usuarios_update.html', usuario=usuario)

    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.funcao = request.form.get('funcao')  

        nova_senha = request.form.get('senha')
        if nova_senha:
            usuario.senha = nova_senha

        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('.recovery', id=id))


@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('.recovery'))

    if request.method == 'GET':
        return render_template('usuarios_delete.html', usuario=usuario)
    
    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
        return redirect(url_for('.recovery'))
