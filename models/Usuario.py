from werkzeug.security import generate_password_hash, check_password_hash
from utils import db


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=db.func.current_timestamp())
    tempo_de_jogo = db.Column(db.Integer, default=0)

    jogos_jogados = db.relationship('Jogar', backref='usuario', lazy=True)

    def __init__(self, nome, email, senha, funcao):
        self.nome = nome
        self.email = email
        self.senha_hash = generate_password_hash(senha)  
        self.funcao = funcao

    def verificar_senha(self, senha):
        """Verifica se a senha fornecida corresponde à senha armazenada"""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.nome} - funcao: {self.funcao}>"

