var titulo = document.getElementById('titulo_principal');
var texto_titulo = titulo.innerHTML;
var i = 0

const escrever = () => {
  titulo.innerHTML = titulo.innerHTML.replace('|', '')

  if (texto_titulo.length > i) {
    if (i == 0){
      titulo.innerHTML = texto_titulo.charAt(i) 
    } else {
      titulo.innerHTML += texto_titulo.charAt(i) 
    }

    titulo.innerHTML += '|'

    i++
    setTimeout(escrever, 60)

  } 
}

escrever()