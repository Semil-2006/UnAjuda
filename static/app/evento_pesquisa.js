const botaoDeBusca = document.getElementById('buscarPerguntas');

function executarBusca() {
    localStorage.setItem('pergunta', botaoDeBusca.value);
    window.location.href = '/pesquisa';
}

botaoDeBusca.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        if (botaoDeBusca.value.length <= 2) {
            alert("Insira mais caracteres");
            naoExecutarBusca(); // Função para executar algo caso a quantidade esteja errada
        } else {
            executarBusca();
        }
    }
});



const perguntaSalva = localStorage.getItem('pergunta');
if (perguntaSalva) {
    console.log("Pergunta:", perguntaSalva);
}
