"use strict";
window.addEventListener('load', () => {
    // Verifica o username e coloca no cabeçalho da página
    const token = localStorage.getItem('token');
    // Recupera o token de autenticação
    fetch(backendAddress + 'accounts/token-auth/', {
        method: 'GET',
        headers: {
            'Authorization': tokenKeyword + token
            // Reenvia o token no cabeçalho HTTP
        }
    })
        .then(response => {
        response.json().then(() => {
            if (response.ok) {
                // token enviado no cabeçalho foi aceito pelo servidor
                let objDiv = document.getElementById('curador');
                objDiv.classList.remove('invisivel');
                objDiv.classList.add('visivelCurador');
            }
            else {
                // token enviado no cabeçalho foi rejeitado pelo servidor
                let objDiv = document.getElementById('curador');
                objDiv.classList.remove('visivelCurador');
                objDiv.classList.add('invisivel');
            }
        });
    })
        .catch(erro => {
        console.log('[setLoggedUser] deu erro: ' + erro);
    });
});
