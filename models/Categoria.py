from utils import db

class Categoria(db.Model):
    __tablename__ = "categoria"
    
    id = db.Column(db.Integer, primary_key=True)
    id_jogo = db.Column(db.Integer, db.ForeignKey('jogo.id'), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    
    def __init__(self, id_jogo, categoria):
        self.id_jogo = id_jogo
        self.categoria = categoria
        
    def __repr__(self):
        return "<Categoria {} - categoria: {}>".format(self.id, self.categoria)
