from utils import db

class Usuario(db.Model):
    __tablename__ = "usuario"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Campo adicionado

    def __init__(self, nome, email, senha, tipo):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
    
    def __repr__(self):
        return "<Usuario {} - Tipo: {}>".format(self.nome, self.tipo)
