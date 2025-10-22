from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  # Corrigido: deve importar de flask_mail

# Inicialização do banco de dados
db = SQLAlchemy()

# Configuração do gerenciador de login
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # rota para redirecionar usuários não logados
login_manager.login_message = "Por favor, faça login para acessar esta página."

# Inicialização do e-mail
mail = Mail()
