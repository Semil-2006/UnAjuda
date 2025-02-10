import sqlite3


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
                id_usuario INTEGER NOT NULL,
                pergunta TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resposta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pergunta INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                resposta TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_pergunta) REFERENCES pergunta(id),
                FOREIGN KEY (id_usuario) REFERENCES usuario(id) 
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

def adicionar_pergunta(conexao, id_usuario, pergunta):
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO pergunta (id_usuario, pergunta)
        VALUES (?, ?)
    ''', (id_usuario, pergunta))
    conexao.commit()
    print(f"Pergunta '{pergunta}' adicionada com sucesso por usuário com ID {id_usuario}!")


def obter_perguntas_com_nome_usuario(conexao):
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT p.id AS pergunta_id, p.pergunta, u.nome AS nome_usuario
        FROM pergunta p
        INNER JOIN usuario u ON p.id_usuario = u.id
        ORDER BY p.id
    ''')
    
    perguntas = cursor.fetchall()
    perguntas_com_nome_usuario = []
    for pergunta in perguntas:
        pergunta_id = pergunta[0]
        pergunta_texto = pergunta[1]
        nome_usuario = pergunta[2]
        perguntas_com_nome_usuario.append({
            "pergunta_id": pergunta_id,
            "pergunta": pergunta_texto,
            "nome_usuario": nome_usuario
        })
    
    return perguntas_com_nome_usuario


def obter_perguntas_com_respostas_e_nome_usuario(conexao, query=None):
    cursor = conexao.cursor()

    if query:
        query = f"%{query}%"
        cursor.execute('''
            SELECT p.id AS pergunta_id, p.pergunta, u.nome AS nome_usuario, p.id_usuario
            FROM pergunta p
            INNER JOIN usuario u ON p.id_usuario = u.id
            LEFT JOIN resposta r ON p.id = r.id_pergunta
            WHERE p.pergunta LIKE ?
            ORDER BY p.data_criacao DESC
        ''', (query,))
    else:
        # Caso contrário, retorne todas as perguntas
        cursor.execute('''
            SELECT p.id AS pergunta_id, p.pergunta, u.nome AS nome_usuario, p.id_usuario
            FROM pergunta p
            INNER JOIN usuario u ON p.id_usuario = u.id
            LEFT JOIN resposta r ON p.id = r.id_pergunta
            ORDER BY p.data_criacao DESC
        ''')

    perguntas_respostas = {}
    for row in cursor.fetchall():
        pergunta_id = row[0]
        pergunta = row[1]
        nome_usuario = row[2]
        usuario_id = row[3]

        # Adiciona a pergunta ao dicionário
        if pergunta_id not in perguntas_respostas:
            perguntas_respostas[pergunta_id] = {
                "pergunta": pergunta,
                "nome_usuario": nome_usuario,
                "usuario_id": usuario_id,
                "respostas": []
            }

    return perguntas_respostas


def adicionar_resposta(conexao, id_pergunta, id_usuario, resposta):
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO resposta (id_pergunta, id_usuario, resposta)
        VALUES (?, ?, ?)
    ''', (id_pergunta, id_usuario, resposta))
    conexao.commit()
    print(f"Resposta '{resposta}' adicionada à pergunta com ID {id_pergunta} por usuário {id_usuario}!")


def buscar_perguntas_por_palavra_chave(conexao, palavra_chave):
    cursor = conexao.cursor()
    palavra_chave = f"%{palavra_chave}%"
    cursor.execute('''
        SELECT p.id, p.pergunta, u.nome
        FROM pergunta p
        INNER JOIN usuario u ON p.id_usuario = u.id
        WHERE p.pergunta LIKE ? 
        ORDER BY p.data_criacao DESC
    ''', (palavra_chave,))

    perguntas = cursor.fetchall()

    perguntas_com_nome_usuario = []
    for pergunta in perguntas:
        perguntas_com_nome_usuario.append({
            "pergunta_id": pergunta[0],
            "pergunta": pergunta[1],
            "nome_usuario": pergunta[2]
        })

    return perguntas_com_nome_usuario


def obter_id_usuario(conexao, email):
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM usuario WHERE email = ?', (email,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    return None


def fechar_conexao(conexao):
    if conexao:
        conexao.close()
