const botaoDeBusca = document.getElementById('buscarPerguntas');

function executarBusca() {
    const pergunta = botaoDeBusca.value;

    // Verificar se a pergunta tem pelo menos 3 caracteres
    if (pergunta.length <= 2) {
        alert("Insira mais caracteres");
        return;
    }

    // Armazenar a pergunta no localStorage
    localStorage.setItem('pergunta', pergunta);

    // Enviar a pergunta via GET para o servidor
    const url = `/pesquisa?query=${encodeURIComponent(pergunta)}`;
    window.location.href = url;  // Navega para a página de pesquisa
}

// Adiciona o evento de pressionamento da tecla Enter para a busca
botaoDeBusca.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        executarBusca();
    }
});

// Recupera a pergunta salva no localStorage e exibe no console
const perguntaSalva = localStorage.getItem('pergunta');
if (perguntaSalva) {
    console.log("Pergunta:", perguntaSalva);
}
