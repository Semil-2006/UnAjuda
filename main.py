from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(_name_)
app.secret_key = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

main = Blueprint('main', _name_)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(150), nullable=False)

@main.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash('As senhas não coincidem. Tente novamente.')
            return redirect(url_for('main.registrar'))

        usuario_existente = Usuario.query.filter_by(nome=nome).first()
        if usuario_existente:
            flash('Usuário já existe. Escolha outro nome.')
            return redirect(url_for('main.registrar'))

        nova_senha = generate_password_hash(senha, method='sha256')
        novo_usuario = Usuario(nome=nome, senha=nova_senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso!')
            return redirect(url_for('main.login'))
        except:
            flash('Erro ao criar conta. Tente novamente.')
            return redirect(url_for('main.registrar'))

    return render_template('registrar.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(nome=nome).first()

        if not usuario or not check_password_hash(usuario.senha, senha):
            flash('Nome de usuário ou senha incorretos.')
            return redirect(url_for('main.login'))

        session['usuario_id'] = usuario.id
        flash('Login realizado com sucesso!')
        return redirect(url_for('main.pagina_inicial'))

    return render_template('login.html')

@main.route('/pagina_inicial')
def pagina_inicial():
    if 'usuario_id' not in session:
        flash('Por favor, faça login para acessar esta página.')
        return redirect(url_for('main.login'))

    return "Bem-vindo à página inicial!"

@main.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado com sucesso!')
    return redirect(url_for('main.login'))

app.register_blueprint(main)

if _name_ == '_main_':
    db.create_all()
    app.run(debug=True)
