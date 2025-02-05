from utils import db

class Jogo(db.Model):
    __tablename__ = "jogo"
    
    id = db.Column(db.Integer, primary_key=True)
    id_criador = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, default=db.func.current_timestamp())
    url_download = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="pendente")
    data_envio = db.Column(db.DateTime, default=db.func.current_timestamp())

    id_desenvolvedor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    def __init__(self, id_criador, titulo, descricao, url_download, status):
        self.id_criador = id_criador
        self.titulo = titulo
        self.descricao = descricao
        self.url_download = url_download
        self.status = status
        
    def __repr__(self):
        return "<Jogo {} - titulo: {}>".format(self.id, self.titulo)
