"use strict";
onload = () => {
    document.getElementById('insere').addEventListener('click', evento => {
        evento.preventDefault();
        // pega todos os elementos do formulário
        const elements = document.getElementById('meuFormulario').elements;
        // dicionário vazio
        let data = {};
        // preenche o dicionário com os pares nome/valor
        for (let i = 0; i < elements.length; i++) {
            const element = elements[i];
            data[element.name] = element.value;
        }
        // envia os dados para o backend
        fetch(backendAddress + "artigos/autor/", {
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
                lugar.innerHTML = 'Dados de autoria inseridos com sucesso';
            }
            else {
                lugar.innerHTML = 'Dados de autoria com erro';
            }
        })
            .catch(error => { console.log(error); });
    });
};
