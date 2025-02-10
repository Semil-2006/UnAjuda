const labelEditarFotoPerfil = document.querySelector('.editar-arquivo-perfil');
const editarFotoPerfil = document.querySelector('#editar-foto-perfil-usuario')
const imagemPerfil = document.querySelector('.img-editar-perfil');

labelEditarFotoPerfil.addEventListener('click', () => {
    editarFotoPerfil.click();
})

// function lerConteudoDoArquivo  (arquivo) {
//     return new Promise((resolve, reject) => {
//         const leitorImagem = new FileReader();
//         leitorImagem.onload = () =>{
//             resolve({url: leitorImagem.result, nome: leitorImagem.name})
//         }

//         leitorImagem.onerror = () =>{
//             reject(`Erro ao carregar a imagem ${arquivo.name}`)
//         }

//         leitorImagem.readAsDataURL(arquivo)
//     })

// }


// editarFotoPerfil.addEventListener('change', async (evento) => {
//     const arquivo = evento.target.files[0]
//     console.log("error")

//     if(arquivo){
//         try {
//             const ConteudoDoArquivo = await lerConteudoDoArquivo(arquivo);
//             imagemPerfil.src = ConteudoDoArquivo.url;
//             evento.target.value = '';
//         } catch (error){
//             console.error("erro na leitura do arquivo");
//         }
//     }
// })