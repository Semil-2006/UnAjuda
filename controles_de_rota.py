from flask import Flask, render_template, request, redirect, flash, session, g
from banco_dados_logi import inicializar_banco_de_dados, adicionar_usuario, obter_usuario_por_email
import bcrypt
import sqlite3
import os
from datetime import timedelta
from functools import wraps

unajuda = Flask(__name__)
unajuda.secret_key = os.getenv('FLASK_SECRET_KEY', 'chave_secreta_segura')
unajuda.permanent_session_lifetime = timedelta(hours=1)

# Banco de Dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('usuario.db', check_same_thread=False)
    return g.db

@unajuda.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Before Request
def make_session_permanent():
    session.permanent = True

unajuda.before_request(make_session_permanent)

# Rota: Home
@unajuda.route('/')
def home():
    return render_template('pagina-principal.html')

@unajuda.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('password')
        confirmar_senha = request.form.get('confirm_password')

        if not nome or not email or not senha or not confirmar_senha:
            flash("Todos os campos são obrigatórios!", "error")
            return redirect('/cadastro')

        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "error")
            return redirect('/cadastro')

        if obter_usuario_por_email(get_db(), email):
            flash("Este email já está cadastrado.", "error")
            return redirect('/cadastro')

        try:
            hashed_senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
            adicionar_usuario(get_db(), nome, email, hashed_senha)
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect('/login')
        except Exception:
            flash("Ocorreu um erro ao processar sua solicitação. Tente novamente.", "error")
            return redirect('/cadastro')

    return render_template('/cadastro')

@unajuda.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        if not email or not senha:
            flash("Email e senha são obrigatórios.", "error")
            return redirect('/login')

        usuario = obter_usuario_por_email(get_db(), email)
        if not usuario:
            flash("Usuário não encontrado.", "error")
            return redirect('/login')

        senha_armazenada = usuario[3]
        if not bcrypt.checkpw(senha.encode(), senha_armazenada):
            flash("Senha incorreta.", "error")
            return redirect('/login')

        session['usuario'] = usuario[1]
        flash(f"Bem-vindo, {usuario[1]}!", "success")
        return redirect('/')

    return render_template('/login')

@unajuda.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da sua conta.", "success")
    return redirect('/login')

if __name__ == '__main__':
    inicializar_banco_de_dados('usuario.db')
    unajuda.run(debug=True)
