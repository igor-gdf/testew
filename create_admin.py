from app import app  # Certifique-se de que o caminho do import esteja correto
from models.Usuario import Usuario
from utils import db

with app.app_context():
    admin_existente = Usuario.query.filter_by(email="admin@example.com").first()
    if not admin_existente:
        admin = Usuario(
            nome="Administrador",
            email="admin@example.com",
            senha="senha_super_segura",  
            funcao="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuário administrador criado com sucesso!")
    else:
        print("Usuário administrador já existe!")
