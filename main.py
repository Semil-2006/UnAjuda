from flask import Flask, request, redirect, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from banco_dados_logi import Usuario, Banco

app = Flask(__name__)
app.secret_key = 'chave_secreta'

engine = create_engine('sqlite:///usuarios.db')
Banco.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

class AuthController:
    def registrar_usuario(self, email, senha, confirmar_senha):
        if senha != confirmar_senha:
            return "As senhas não coincidem"

        usuario_existente = db_session.query(Usuario).filter_by(email=email).first()
        if usuario_existente:
            return "Usuário já cadastrado"

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=email.split('@')[0], email=email, senha=senha_hash)
        db_session.add(novo_usuario)
        db_session.commit()

        session['usuario_id'] = novo_usuario.id
        return redirect('/login')

    def autenticar_usuario(self, email, senha):
        usuario = db_session.query(Usuario).filter_by(email=email).first()

        if not usuario or not check_password_hash(usuario.senha, senha):
            return "Credenciais inválidas"

        session['usuario_id'] = usuario.id
        return redirect('/pagina-principal')

controller = AuthController()

@app.route('/')
def inicio():
    return redirect('/registro')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        return controller.registrar_usuario(email, senha, confirmar_senha)
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        return controller.autenticar_usuario(email, senha)
    return render_template('login.html')

@app.route('/pagina-principal')
def pagina_principal():
    if 'usuario_id' not in session:
        return redirect('/login')
    return render_template('pagina-principal.html')

if __name__ == '__main__':
    app.run(debug=True)
