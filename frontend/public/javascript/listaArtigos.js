"use strict";
onload = function () {
    let buscar = document.getElementById('buscar');
    buscar.addEventListener('click', exibeListaDeArtigos);
    let urlParams = new URLSearchParams(window.location.search);
    let idAutor = urlParams.get('idAutor');
    let nomeAutor = document.getElementById('autor-escolhido');
    if (idAutor !== null && idAutor !== "")
        fetch(backendAddress + 'artigos/autor/' + idAutor)
            .then(response => response.json())
            .then((autor) => nomeAutor.innerText = " de " + autor.nome);
    else {
        nomeAutor.innerText = "";
    }
    exibeListaDeArtigos(); // exibe lista de Artigos ao carregar a página
};
async function exibeListaDeArtigos() {
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
    if (!usuario.curador) {
        document.getElementById('curador').style.display = "none";
    }
    let titulo = document.getElementsByName('titulo')[0];
    let autor = document.getElementsByName('autor')[0];
    const queryString = new URLSearchParams({
        titulo: titulo.value || "",
        autor: autor.value || ""
    }).toString();
    let artigos = await fetch(backendAddress + "artigos/artigos/?" + queryString)
        .then(response => response.json());
    let tbody = document.getElementById('idtbody');
    tbody.innerHTML = "";
    // se a página foi aberta a partir de um autor
    let urlParams = new URLSearchParams(window.location.search);
    let idAutor = urlParams.get('idAutor');
    if (idAutor !== null || idAutor === "") {
        artigos = artigos.filter(at => at.autores.some(au => au.id === parseInt(idAutor)));
    }
    if (artigos.length === 0) {
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.colSpan = 4;
        td.style.textAlign = "center";
        td.innerText = "Sem resultados";
        tr.appendChild(td);
        tbody.appendChild(tr);
    }
    else
        for (let Artigo of artigos) {
            let tr = document.createElement('tr');
            appendTextCell(tr, Artigo.nome);
            appendTextCell(tr, Artigo.ano_publicacao.toString());
            let autores = Artigo.autores
                .map((autor) => autor.nome)
                .join('; ');
            if (autores === "")
                autores = "Sem autores cadastrados";
            appendTextCell(tr, autores);
            // Ícones de ações:
            let tdAções = document.createElement('td');
            tdAções.style.textAlign = "center";
            let link = document.createElement('a');
            link.href = Artigo.link;
            link.target = "_blank";
            if (Artigo.link === null || Artigo.link === "" || Artigo.link === undefined)
                link.style.visibility = "hidden";
            let icon = document.createElement('img');
            icon.src = "images/view.png";
            icon.alt = "Visitar o artigo";
            link.appendChild(icon);
            tdAções.appendChild(link);
            let edit = document.createElement('a');
            edit.href = "atualizaArtigo.html?id=" + Artigo.id;
            let iconEdit = document.createElement('img');
            iconEdit.src = "images/edit.png";
            iconEdit.alt = "Editar o artigo";
            edit.appendChild(iconEdit);
            tdAções.appendChild(edit);
            // Esse ícone ficou como parágrafo porque o clique nele não leva
            // para outra página, e ajudou na hora de alinhar os ícones numa
            // mesma linha.
            let del = document.createElement('p');
            del.style.display = "inline";
            let deleteIcon = document.createElement('img');
            deleteIcon.src = "images/bin.png";
            deleteIcon.alt = "Remover o artigo";
            deleteIcon.style.cursor = "pointer";
            deleteIcon.style.display = "inline";
            deleteIcon.addEventListener('click', () => {
                fetch(backendAddress + 'artigos/artigo/' + Artigo.id, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': tokenKeyword + localStorage.getItem('token'),
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => { exibeListaDeArtigos(); })
                    .catch(error => { console.log(error); });
            });
            del.appendChild(deleteIcon);
            tdAções.appendChild(del);
            if (!usuario.curador) {
                deleteIcon.style.display = "none";
                edit.style.display = "none";
            }
            tr.appendChild(tdAções);
            tbody.appendChild(tr);
        }
}
