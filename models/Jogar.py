from utils import db

class Jogar(db.Model):
    __tablename__ = "jogar"
    
    id = db.Column(db.Integer, primary_key=True)
    tempo_de_jogo = db.Column(db.Integer, nullable=False)
    id_jogo = db.Column(db.Integer, db.ForeignKey('jogo.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    def __init__(self, tempo_de_jogo, id_jogo, id_usuario):
        self.tempo_de_jogo = tempo_de_jogo
        self.id_jogo = id_jogo
        self.id_usuario = id_usuario
        
    def __repr__(self):
        return "<Jogar {} - tempo: {}>".format(self.id, self.tempo_de_jogo)
