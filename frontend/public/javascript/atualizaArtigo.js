"use strict";
onload = async () => {
    // Carrega os dados do banco de dados
    // e preenche o formulário
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    const idPlace = document.getElementById('mensagem');
    if (id) {
        let promiseArtigo = fetch(backendAddress + 'artigos/artigo/' + id + '/', { method: 'GET', headers: { 'Content-Type': 'application/json' } });
        let promiseAutores = fetch(backendAddress + 'artigos/autores/', { method: 'GET', headers: { 'Content-Type': 'application/json' } });
        let artigo = await promiseArtigo.then(res => res.json());
        let todosAutores = await promiseAutores.then(res => res.json());
        let get = (id) => document.getElementById(id);
        get('nome').value = artigo.nome;
        get('ano_publicacao').value = artigo.ano_publicacao.toString();
        get('link').value = artigo.link;
        let select = document.getElementById('autores');
        for (let autor of todosAutores) {
            let option = document.createElement('option');
            option.value = autor.id.toString();
            option.text = autor.nome;
            option.selected = artigo.autores.some(a => a.id == autor.id);
            select.add(option);
        }
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
            if (element.name == 'autores') {
                let select = element;
                let selectedOptions = Array.from(select.selectedOptions);
                data[element.name] = selectedOptions.map(o => parseInt(o.value));
            }
            else {
                data[element.name] = element.value;
            }
        }
        fetch(backendAddress + "artigos/artigo/" + id + '/', {
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
