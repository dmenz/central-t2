"use strict";
onload = function () {
    exibeListaDeAutores(); // exibe lista de Autores ao carregar a página
};
const remove = () => {
    let idArray = [];
    let checkboxes = document.getElementsByTagName('input');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            idArray.push(checkboxes[i].value);
        }
    }
    fetch(backendAddress + 'autores/lista/', {
        method: 'DELETE',
        headers: {
            'Authorization': tokenKeyword + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(idArray)
    })
        .then(response => { exibeListaDeAutores(); })
        .catch(error => { console.log(error); });
};
function exibeListaDeAutores() {
    const appendTextCell = (tr, text) => {
        let td = document.createElement('td');
        td.appendChild(document.createTextNode(text));
        tr.appendChild(td);
    };
    fetch(backendAddress + "artigos/autores/")
        .then(response => response.json())
        .then(Autores => {
        let tbody = document.getElementById('idtbody');
        tbody.innerHTML = "";
        for (let Autor of Autores) {
            let tr = document.createElement('tr');
            appendTextCell(tr, Autor.nome);
            // TODO: valor abaixo é provisório, deve ser quantidade de artigos
            let qtd = document.createElement('td');
            qtd.style.textAlign = "center";
            qtd.innerText = "7";
            tr.appendChild(qtd);
            // Ícones de ações:
            let tdAções = document.createElement('td');
            tdAções.style.textAlign = "center";
            let link = document.createElement('a');
            link.href = Autor.link;
            link.target = "_blank";
            if (Autor.link === null || Autor.link === "" || Autor.link === undefined)
                link.style.visibility = "hidden";
            let icon = document.createElement('img');
            icon.src = "images/view.png";
            icon.alt = "Ver textos deste autor";
            link.appendChild(icon);
            tdAções.appendChild(link);
            let edit = document.createElement('a');
            edit.href = "insereAutor.html?id=" + Autor.id;
            let iconEdit = document.createElement('img');
            iconEdit.src = "images/edit.png";
            iconEdit.alt = "Editar o autor";
            edit.appendChild(iconEdit);
            tdAções.appendChild(edit);
            // Esse ícone ficou como parágrafo porque o clique nele não leva
            // para outra página, e ajudou na hora de alinhar os ícones numa
            // mesma linha.
            let del = document.createElement('p');
            del.style.display = "inline";
            let deleteIcon = document.createElement('img');
            deleteIcon.src = "images/bin.png";
            deleteIcon.alt = "Remover o autor";
            deleteIcon.style.cursor = "pointer";
            deleteIcon.style.display = "inline";
            deleteIcon.addEventListener('click', () => {
                fetch(backendAddress + 'artigos/autor/' + Autor.id, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': tokenKeyword + localStorage.getItem('token'),
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => { exibeListaDeAutores(); })
                    .catch(error => { console.log(error); });
            });
            del.appendChild(deleteIcon);
            tdAções.appendChild(del);
            tr.appendChild(tdAções);
            tbody.appendChild(tr);
        }
    })
        .catch(error => {
        console.error("Erro:", error);
    });
}
