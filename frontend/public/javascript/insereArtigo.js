"use strict";
onload = async () => {
    let todosAutores = await fetch(backendAddress + 'artigos/autores/', { method: 'GET', headers: { 'Content-Type': 'application/json' } })
        .then(response => response.json());
    let select = document.getElementById('autores');
    for (let autor of todosAutores) {
        let option = document.createElement('option');
        option.value = autor.id.toString();
        option.text = autor.nome;
        select.add(option);
    }
    document.getElementById('insere').addEventListener('click', evento => {
        evento.preventDefault();
        // pega todos os elementos do formulário
        const elements = document.getElementById('meuFormulario').elements;
        // dicionário vazio
        let data = {};
        // preenche o dicionário com os pares nome/valor
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
        // envia os dados para o backend
        fetch(backendAddress + "artigos/artigo/", {
            method: 'POST',
            headers: {
                'Authorization': tokenKeyword + localStorage.getItem('token'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => {
            let lugar = document.getElementById('mensagem');
            if (response.ok) {
                lugar.innerHTML = 'Dados de artigo inseridos com sucesso';
            }
            else {
                lugar.innerHTML = 'Dados de artigo com erro';
            }
        })
            .catch(error => { console.log(error); });
    });
};
