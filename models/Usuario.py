from utils import db

class Usuario(db.Model):
    __tablename__ = "usuario"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    funcao = db.Column(db.String(50), nullable=False)  

    def __init__(self, nome, email, senha, funcao):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.funcao = funcao
    
    def __repr__(self):
        return "<Usuario {} - funcao: {}>".format(self.nome, self.funcao)
