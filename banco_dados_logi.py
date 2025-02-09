import sqlite3
import bcrypt


def inicializar_banco_de_dados(nome_arquivo='usuario.db'):
    with sqlite3.connect(nome_arquivo) as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                faculdade TEXT,
                curso TEXT,
                telefone TEXT,
                foto_perfil TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pergunta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pergunta TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resposta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pergunta INTEGER NOT NULL,
                resposta TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_pergunta) REFERENCES pergunta(id)
            )
        ''')

        conexao.commit()
    return sqlite3.connect(nome_arquivo, check_same_thread=False)


def adicionar_usuario(conexao, nome, email, senha):
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuario (nome, email, senha)
            VALUES (?, ?, ?)
        ''', (nome, email, senha))
        conexao.commit()
        print(f"Usuário '{nome}' adicionado com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao adicionar o usuário '{nome}': {e}")


def obter_usuarios(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT id, nome, email FROM usuario')
    return cursor.fetchall()


def obter_usuario_por_email(conexao, email):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuario WHERE email = ?', (email,))
    return cursor.fetchone()

def fechar_conexao(conexao):
    if conexao:
        conexao.close()
