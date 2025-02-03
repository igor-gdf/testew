from utils import db

class Adm(db.Model):
    __tablename__ = "adm"
    
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    
    def __init__(self, id_usuario, telefone):
        self.id_usuario = id_usuario
        self.telefone = telefone
        
    def __repr__(self):
        return "<Adm {} - id_usuario: {}>".format(self.id, self.id_usuario)
