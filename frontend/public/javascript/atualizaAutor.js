"use strict";
onload = () => {
    // Carrega os dados do banco de dados
    // e preenche o formulário
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const idPlace = document.getElementById('mensagem');
    if (id) {
        fetch(backendAddress + 'artigos/autor/' + id, {
            method: 'GET',
            headers: {
                'Authorization': tokenKeyword + localStorage.getItem('token'),
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then((autor) => {
            let campoNome = document.getElementById('nome');
            campoNome.value = autor.nome;
        })
            .catch(erro => {
            console.log('Deu erro: ' + erro);
        });
    }
    else {
        idPlace.innerHTML = 'URL mal formada: ' + window.location;
    }
    document.getElementById('atualiza')
        .addEventListener('click', (evento) => {
        evento.preventDefault();
        const form = document.getElementById('meuFormulario');
        const elements = form.elements;
        let data = {};
        for (let i = 0; i < elements.length; i++) {
            const element = elements[i];
            data[element.name] = element.value;
        }
        fetch(backendAddress + 'artigos/autor/' + id + '/', {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: {
                'Authorization': tokenKeyword + localStorage.getItem('token'),
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
            if (response.ok) {
                document.getElementById('mensagem').innerHTML = 'Sucesso';
            }
            else {
                document.getElementById('mensagem').innerHTML = 'Erro: '
                    + response.status + " " + response.statusText;
            }
        })
            .catch(erro => {
            console.log('Deu erro: ' + erro);
        });
    });
};
