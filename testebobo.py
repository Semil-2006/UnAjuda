from banco_dados_logi import obter_usuario_por_email,adicionar_usuario, adicionar_pergunta, adicionar_resposta, inicializar_banco_de_dados, obter_perguntas_com_respostas_e_nome_usuario, fechar_conexao

conexao = inicializar_banco_de_dados()


usuarios = [
    ("Semil", "semil@exemplo.com", "senha123"),
    ("João", "joao@exemplo.com", "senha123"),
    ("Maria", "maria@exemplo.com", "senha123"),
    ("Carlos", "carlos@exemplo.com", "senha123"),
    ("Ana", "ana@exemplo.com", "senha123")
]

usuario_ids = []
for nome, email, senha in usuarios:
    adicionar_usuario(conexao, nome, email, senha)
    usuario = obter_usuario_por_email(conexao, email)
    usuario_ids.append(usuario[0])

perguntas = [
    "Qual é a capital do Brasil?",
    "Qual é a maior montanha do mundo?",
    "Quem inventou a lâmpada elétrica?",
    "Qual é o maior oceano do planeta?",
    "Quem pintou a Mona Lisa?"
]

for i, pergunta in enumerate(perguntas):
    adicionar_pergunta(conexao, usuario_ids[i], pergunta)

respostas = [
    ("Brasília", "Monte Everest", "Thomas Edison", "Oceano Pacífico", "Leonardo da Vinci"),
    ("São Paulo", "K2", "Nikola Tesla", "Oceano Atlântico", "Pablo Picasso"),
    ("Rio de Janeiro", "Mont Blanc", "Michael Faraday", "Oceano Índico", "Vincent van Gogh"),
    ("Salvador", "Aconcágua", "James Watt", "Oceano Ártico", "Claude Monet"),
    ("Belo Horizonte", "Denali", "Benjamin Franklin", "Oceano Antártico", "Rembrandt")
]

for i in range(5):
    for j in range(5):
        if i != j:
            resposta = respostas[j][i]
            adicionar_resposta(conexao, i + 1, usuario_ids[j], resposta)

perguntas_respostas = obter_perguntas_com_respostas_e_nome_usuario(conexao)
for pergunta_id, dados in perguntas_respostas.items():
    print(f"Pergunta: {dados['pergunta']} (Feita por {dados['nome_usuario']})")
    for resposta in dados['respostas']:
        print(f"  Resposta: {resposta}")

fechar_conexao(conexao)
