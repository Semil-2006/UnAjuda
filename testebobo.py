from banco_dados_logi import adicionar_pergunta, adicionar_resposta, inicializar_banco_de_dados, obter_perguntas_com_respostas_e_nome_usuario, fechar_conexao

# Inicializa o banco de dados
conexao = inicializar_banco_de_dados()
cursor = conexao.cursor()

cursor.execute('''
    INSERT INTO usuario (nome, email, senha)
    VALUES (?, ?, ?)
''', ("Semil", "241025499@aluno.unb.br", "3122"))
conexao.commit()
usuario_id_1 = cursor.lastrowid

usuarios = [
    ("João", "joao@exemplo.com", "senha123"),
    ("Maria", "maria@exemplo.com", "senha123"),
    ("Carlos", "carlos@exemplo.com", "senha123")
]

usuario_ids = []
for nome, email, senha in usuarios:
    cursor.execute('''
        INSERT INTO usuario (nome, email, senha)
        VALUES (?, ?, ?)
    ''', (nome, email, senha))
    conexao.commit()
    usuario_ids.append(cursor.lastrowid)

perguntas = [
    ("Qual é a capital do Brasil?"),
    ("Qual é a maior montanha do mundo?"),
    ("Quem inventou a lâmpada elétrica?"),
    ("Qual é o maior oceano do planeta?")
]

for i, pergunta in enumerate(perguntas):
    adicionar_pergunta(conexao, usuario_ids[i] if i < 3 else usuario_id_1, pergunta)
    for j in range(4):
        if j != i:  # O próprio usuário não responde à sua pergunta
            resposta = f"Resposta do usuário {j+1}"
            adicionar_resposta(conexao, i + 1, resposta)

perguntas_respostas = obter_perguntas_com_respostas_e_nome_usuario(conexao)
for pergunta_id, dados in perguntas_respostas.items():
    print(f"Pergunta: {dados['pergunta']} (Feita por {dados['nome_usuario']})")
    for resposta in dados['respostas']:
        print(f"  Resposta: {resposta}")

fechar_conexao(conexao)

