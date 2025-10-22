from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models.users import User
from utils.token_utils import generate_token, confirm_token  # importe aqui


def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for("users.dashboard"))
        else:
            flash("Email ou senha inválidos.", "danger")
    return render_template("auth/login.html")

def logout():
    logout_user()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("auth.login"))

def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            token = generate_token(email)
            reset_url = url_for("auth.reset_password", token=token, _external=True)
            # Aqui você enviaria o link por e-mail, mas vamos só simular
            flash(f"Link de redefinição: {reset_url}", "info")
        else:
            flash("Email não encontrado.", "danger")

        return redirect(url_for("auth.login"))

    return render_template("auth/forgot_password.html")

def reset_password(token):
    email = confirm_token(token)
    if not email:
        flash("Link inválido ou expirado.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        new_password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            flash("Senha redefinida com sucesso!", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", token=token)
