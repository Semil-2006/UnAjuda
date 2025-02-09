const botaoDeBusca = document.getElementById('buscarPerguntas');

botaoDeBusca.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            if(botaoDeBusca.value.length <= 2){
                alert("insira mais caracteres")
                naoExecutarBusca() //funcao para executar alguma coisa caso a quantidade esteja errada
            }else{
                alert("quantidade de caracteres correta")
                executarBusca() //funcao para executar alguma coisa caso a quantidade esteja correta
            }
        }
})


