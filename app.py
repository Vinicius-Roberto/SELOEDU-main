# app.py
from flask import Flask, render_template
from models.users import db, User
from extensions import login_manager, mail
from routes.auth import auth_bp
from routes.users import users_bp
from config import Config  # ✅ Importa suas configurações


def create_app():
    app = Flask(__name__)

    # ==========================
    # ⚙️ CONFIGURAÇÕES DA APLICAÇÃO
    # ==========================
    app.config.from_object(Config)

    # ==========================
    # 🔧 INICIALIZAÇÃO DAS EXTENSÕES
    # ==========================
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)  # ✅ Agora o Flask-Mail é inicializado corretamente

    # ==========================
    # 🔗 REGISTRO DE BLUEPRINTS
    # ==========================
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    # ==========================
    # 👤 LOGIN MANAGER
    # ==========================
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ==========================
    # 👑 CRIA USUÁRIO MASTER SE NÃO EXISTIR
    # ==========================
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email="admin@seloedu.com").first():
            master = User(
                nome="Admin Master",
                email="admin@seloedu.com",
                role="master"
            )
            master.set_password("123456")
            db.session.add(master)
            db.session.commit()

    # ==========================
    # 🏠 ROTA PRINCIPAL
    # ==========================
    @app.route("/")
    def home():
        return render_template("home.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
