from flask import Flask, render_template, request, redirect, flash, session, g
from banco_dados_logi import inicializar_banco_de_dados, adicionar_usuario, obter_usuario_por_email
import bcrypt
import sqlite3


app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

# Banco de Dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('usuario.db', check_same_thread=False)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Rota: Home
@app.route('/')
def home():
    return render_template('pagina-principal.html')

@app.route('/cadastro', methods=['GET', 'POST'])
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

        try:
            adicionar_usuario(get_db(), nome, email, senha)
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Este email já está cadastrado.", "error")
            return redirect('/cadastro')
        except Exception as e:
            flash(f"Erro ao cadastrar: {str(e)}", "error")
            return redirect('/cadastro')

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
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

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da sua conta.", "success")
    return redirect('/')

if __name__ == '__main__':
    inicializar_banco_de_dados('usuario.db')
    app.run(debug=True)
