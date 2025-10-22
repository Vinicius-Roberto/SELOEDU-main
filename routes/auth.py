from flask import Blueprint
from views.auth import login, logout, forgot_password, reset_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Associando endpoints às funções do views
auth_bp.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
auth_bp.add_url_rule("/logout", view_func=logout)
auth_bp.add_url_rule("/forgot_password", view_func=forgot_password, methods=["GET", "POST"])
auth_bp.add_url_rule("/reset_password/<token>", view_func=reset_password, methods=["GET", "POST"])

