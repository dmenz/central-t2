"use strict";
onload = function () {
    exibeListaDeAutores(); // exibe lista de Autores ao carregar a página
};
async function exibeListaDeAutores() {
    const appendTextCell = (tr, text) => {
        let td = document.createElement('td');
        td.appendChild(document.createTextNode(text));
        tr.appendChild(td);
    };
    const usuario = await fetch(backendAddress + 'accounts/token-auth/', {
        method: 'GET',
        headers: {
            'Authorization': tokenKeyword + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        }
    }).then(response => response.json());
    if (usuario.curador) {
        document.getElementById('curador').style.display = "inline-block";
    }
    let Autores = await fetch(backendAddress + "artigos/autores/")
        .then(response => response.json());
    let tbody = document.getElementById('idtbody');
    tbody.innerHTML = "";
    for (let Autor of Autores) {
        let tr = document.createElement('tr');
        appendTextCell(tr, Autor.nome);
        let qtd = document.createElement('td');
        qtd.style.textAlign = "center";
        qtd.innerText = Autor.n_artigos.toString();
        tr.appendChild(qtd);
        // Ícones de ações:
        let tdAções = document.createElement('td');
        tdAções.style.textAlign = "center";
        let link = document.createElement('a');
        link.href = "listaArtigos.html?idAutor=" + Autor.id;
        let icon = document.createElement('img');
        icon.src = "images/view.png";
        icon.alt = "Ver textos deste autor";
        link.appendChild(icon);
        tdAções.appendChild(link);
        let edit = document.createElement('a');
        edit.href = "atualizaAutor.html?id=" + Autor.id;
        let iconEdit = document.createElement('img');
        iconEdit.src = "images/edit.png";
        iconEdit.alt = "Editar o autor";
        edit.appendChild(iconEdit);
        tdAções.appendChild(edit);
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
                .then(exibeListaDeAutores)
                .catch(error => { console.log(error); });
        });
        tdAções.appendChild(deleteIcon);
        if (!usuario.curador) {
            deleteIcon.style.display = "none";
            edit.style.display = "none";
        }
        tr.appendChild(tdAções);
        tbody.appendChild(tr);
    }
}
