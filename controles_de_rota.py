from flask import Flask, render_template, request, redirect, flash, session, g, jsonify
from banco_dados_logi import inicializar_banco_de_dados, adicionar_usuario, obter_usuario_por_email, obter_id_usuario
import sqlite3
from banco_dados_logi import obter_perguntas_com_respostas_e_nome_usuario, adicionar_pergunta, adicionar_resposta
from datetime import datetime
from time import sleep
import os
from werkzeug.utils import secure_filename
from datetime import timedelta
import bcrypt

unajuda = Flask(__name__)
unajuda.secret_key = os.getenv('FLASK_SECRET_KEY', 'chave_secreta_segura')
unajuda.permanent_session_lifetime = timedelta(weeks=1)
conexao = inicializar_banco_de_dados()


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('usuario.db', check_same_thread=False)
    return g.db


@unajuda.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# usuario_id = session.get('usuario_id')

def make_session_permanent():
    session.permanent = True
    if 'logado' in session:
        if session['logado'] and 'expiracao' in session:
            expiracao = datetime.strptime(session['expiracao'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() > expiracao:
                session.pop('logado', None)
                session.pop('expiracao', None)
                flash("Sua sessão expirou. Por favor, faça login novamente.", "error")


unajuda.before_request(make_session_permanent)


@unajuda.route('/')
@unajuda.route('/home')
def home():
    if 'logado' in session and session['logado']:
        email_logado = session.get('email_usuario')
        usuario = obter_usuario_por_email(inicializar_banco_de_dados(), email_logado)

        if usuario:
            foto_perfil = usuario[7] if usuario[7] else 'uploads/avatar-default-icon.png'
            caminho_completo = f"/static/{foto_perfil}"
            return render_template('pagina-pricinpal-logado.html', foto_perfil=caminho_completo)

    else:
        return render_template('pagina-principal.html')

    return render_template('pagina-principal.html')


@unajuda.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('password')
        confirmar_senha = request.form.get('confirm_password')

        print(f" nome: {nome} Email: {email} senha {senha}")

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
            print("ta caindo aqui")
            adicionar_usuario(get_db(), nome, email, hashed_senha)
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect('/login')
        except Exception:
            flash("Ocorreu um erro ao processar sua solicitação. Tente novamente.", "error")
            return redirect('/cadastro')

    return render_template('cadastro.html')


@unajuda.route('/pergunta', methods=['GET', 'POST'])
def pagina_pergunta():
    if request.method == 'POST':
        if 'usuario_id' not in session:
            session['url_antes_login'] = request.url
            flash("Você precisa estar logado para fazer uma pergunta.", "error")
            return redirect('/login')

        pergunta = request.form.get('pergunta')
        usuario_id = session['usuario_id']

        if not pergunta:
            flash("A pergunta não pode estar vazia.", "error")
            return redirect('/pergunta')

        db = get_db()
        adicionar_pergunta(db, usuario_id, pergunta)
        flash("Pergunta enviada com sucesso!", "success")
        return redirect('/')

    return render_template('pagina-perguntas.html')


@unajuda.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        if not email or not senha:
            flash("Email e senha são obrigatórios.", "error")
            sleep(5)
            return redirect('/login')

        usuario = obter_usuario_por_email(get_db(), email)
        if not usuario:
            flash("Usuário não encontrado.", "error")
            return redirect('/login')

        senha_armazenada = usuario[3]
        if not bcrypt.checkpw(senha.encode(), senha_armazenada):
            flash("Senha incorreta.", "error")
            return redirect('/login')

        session['email_usuario'] = usuario[2]
        session['usuario'] = usuario[1]
        session['logado'] = True
        session['usuario_id'] = usuario[0]
        print(session['usuario_id'])
        session['expiracao'] = (datetime.now() + timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S')
        flash(f"Bem-vindo, {usuario[1]}!", "success")
        url_destino = session.pop('url_antes_login', '/')
        return redirect(url_destino)
    return render_template('login.html')


@unajuda.route('/perfil', methods=['GET', 'POST'])
def pagina_de_perfil():
    if 'logado' in session and session['logado']:
        email_logado = session.get('email_usuario')
        usuario = obter_usuario_por_email(inicializar_banco_de_dados(), email_logado)

        if usuario:
            foto_perfil = usuario[7] if usuario[7] else 'uploads/avatar-default-icon.png'
            caminho_completo = f"/static/{foto_perfil}"
            return render_template('pagina-perfil.html', foto_perfil=caminho_completo)

        return render_template('pagina-perfil.html', usuario=usuario)
    else:
        session['url_antes_login'] = request.url
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect('/login')


def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
unajuda.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
unajuda.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@unajuda.route('/testePerfil', methods=['POST', 'GET'])
def testePerfil():
    return render_template('editar-pagina-perfil.html')


@unajuda.route('/editar-perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'logado' not in session or not session['logado']:
        session['url_antes_login'] = request.url
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect('/login')

    db = inicializar_banco_de_dados()
    emailLogado = session.get('email_usuario')
    idUsuario = obter_id_usuario(db, emailLogado)
    usuario = obter_usuario_por_email(inicializar_banco_de_dados(), emailLogado)
    arquivo = request.files.get('fotoPerfil')

    if arquivo:
        extensao = arquivo.filename.split('.')[-1].lower()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Admito, peguei do GPT
        novoNomeFotoPerfil = f'Foto_perfil{idUsuario}_{timestamp}.{extensao}'
        caminhoFoto = os.path.join('static/uploads/', novoNomeFotoPerfil)
        caminho = f'uploads/{novoNomeFotoPerfil}'
        foto_atual = usuario[7]
        if foto_atual and os.path.exists(f"static/uploads/{foto_atual}"):
            os.remove(f"static/uploads/{foto_atual}")

        arquivo.save(caminhoFoto)
        db.execute("UPDATE usuario SET foto_perfil = ? WHERE id = ?", (caminho, idUsuario))
        db.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect('/perfil')

    # if request.method == 'POST':
    #     nome = request.form.get('nome')
    #     faculdade = request.form.get('faculdade')
    #     curso = request.form.get('curso')
    #     nova_senha = request.form.get('nova_senha')
    #     confirmar_senha = request.form.get('confirmar_senha')
    #     telefone = request.form.get('telefone')
    #     senha_atual = request.form.get('senha_atual')
    #     foto_perfil = request.files.get('foto_perfil')

    #     usuario = obter_usuario_por_email(inicializar_banco_de_dados(), session['usuario'])
    #     senha_armazenada = usuario[3]

    #     if not bcrypt.checkpw(senha_atual.encode(), senha_armazenada):
    #         flash("Senha atual incorreta.", "error")
    #         return redirect('/editar-perfil')

    #     db = inicializar_banco_de_dados()
    #     cursor = db.cursor()
    #     parametros_atualizacao = []

    #     if nome and nome != usuario[1]:
    #         parametros_atualizacao.append(f"nome='{nome}'")
    #     if faculdade and faculdade != usuario[4]:
    #         parametros_atualizacao.append(f"faculdade='{faculdade}'")
    #     if curso and curso != usuario[5]:
    #         parametros_atualizacao.append(f"curso='{curso}'")
    #     if telefone and telefone != usuario[6]:
    #         parametros_atualizacao.append(f"telefone='{telefone}'")

    #     if foto_perfil and foto_perfil.filename:
    #         nome_arquivo = secure_filename(foto_perfil.filename)
    #         caminho_foto = os.path.join(unajuda.config['UPLOAD_FOLDER'], nome_arquivo)
    #         foto_perfil.save(caminho_foto)
    #         parametros_atualizacao.append(f"foto_perfil='{nome_arquivo}'")

    #     if parametros_atualizacao:
    #         query = "UPDATE usuario SET " + ", ".join(parametros_atualizacao) + " WHERE email=?"
    #         cursor.execute(query, (session['usuario'],))

    #     if nova_senha and nova_senha == confirmar_senha:
    #         senha_criptografada = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt())
    #         cursor.execute("UPDATE usuario SET senha=? WHERE email=?", (senha_criptografada, session['usuario']))

    #     db.commit()

    return render_template('editar-pagina-perfil.html')


def responder_pergunta(pergunta_id):
    if 'usuario_id' not in session:
        return jsonify({"success": False, "message": "Usuário não autenticado!"}), 401

    data = request.get_json()
    resposta_texto = data.get("resposta")

    if not resposta_texto:
        return jsonify({"success": False, "message": "A resposta não pode estar vazia!"}), 400

    usuario_id = session['usuario_id']
    db = get_db()
    adicionar_resposta(db, pergunta_id, usuario_id, resposta_texto)

    return jsonify({"success": True, "message": "Resposta adicionada com sucesso!"})


@unajuda.route('/pesquisa')
def pesquisa():
    db = get_db()
    query = request.args.get('query', '').strip()

    if query:
        perguntas_respostas = obter_perguntas_com_respostas_e_nome_usuario(db, query)
    else:
        perguntas_respostas = obter_perguntas_com_respostas_e_nome_usuario(db)

    perguntas = []
    usuario_logado_id = session.get('usuario_id')

    for pergunta_id, dados in perguntas_respostas.items():
        usuario_id = dados.get('usuario_id')
        nome_usuario = "Você" if usuario_id == usuario_logado_id else dados['nome_usuario']

        perguntas.append({
            "id": pergunta_id,
            "pergunta": dados['pergunta'],
            "nome_usuario": nome_usuario
        })

    return render_template('pagina-pesquisa.html', perguntas=perguntas)

@unajuda.route('/resposta/<int:pergunta_id>')
def pagina_resposta(pergunta_id):
    db = get_db()
    perguntas_respostas = obter_perguntas_com_respostas_e_nome_usuario(db)

    if pergunta_id not in perguntas_respostas:
        flash("Pergunta não encontrada!", "error")
        return redirect('/pesquisa')

    pergunta = perguntas_respostas[pergunta_id]
    pergunta["id"] = pergunta_id  # Garante que o ID está presente

    usuario_logado_id = session.get('usuario_id')

    cursor = db.cursor()
    cursor.execute("""
        SELECT resposta.resposta, usuario.nome, resposta.id_usuario
        FROM resposta
        JOIN usuario ON resposta.id_usuario = usuario.id
        WHERE resposta.id_pergunta = ?
        ORDER BY resposta.id DESC
    """, (pergunta_id,))

    respostas = cursor.fetchall()

    return render_template('pagina-resposta.html', pergunta=pergunta, respostas=respostas)

@unajuda.route('/responder/<int:pergunta_id>', methods=['POST'])
def responder_pergunta(pergunta_id):
    if 'usuario_id' not in session:
        return jsonify({"success": False, "message": "Usuário não autenticado!"}), 401

    data = request.get_json()
    resposta_texto = data.get("resposta")

    if not resposta_texto:
        return jsonify({"success": False, "message": "A resposta não pode estar vazia!"}), 400

    usuario_id = session['usuario_id']
    db = get_db()
    adicionar_resposta(db, pergunta_id, usuario_id, resposta_texto)

    return jsonify({"success": True, "message": "Resposta adicionada com sucesso!"})

@unajuda.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('logado', None)
    session.pop('expiracao', None)
    flash("Você saiu da sua conta.", "success")
    sleep(5)
    return redirect('/')


if __name__ == '__main__':
    inicializar_banco_de_dados('usuario.db')
    unajuda.run(debug=True)