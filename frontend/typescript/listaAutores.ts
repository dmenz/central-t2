onload = function () {
    exibeListaDeAutores(); // exibe lista de Autores ao carregar a página
}


const remove = () => {
    let idArray =  [];
    let checkboxes = document.getElementsByTagName('input');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            idArray.push(checkboxes[i].value)
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
    .then(response => { exibeListaDeAutores() })
    .catch(error => { console.log(error) })
}


async function exibeListaDeAutores() {
    const appendTextCell = (tr: HTMLTableRowElement, text: string) => {
        let td = document.createElement('td') as HTMLTableCellElement;
        td.appendChild(document.createTextNode(text));
        tr.appendChild(td);
    }

    const usuario = await fetch(backendAddress + 'accounts/token-auth/', {
        method: 'GET',
        headers: {
            'Authorization': tokenKeyword + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()) as Usuario;
    if (!usuario.curador) {
        document.getElementById('curador')!.style.display = "none";
    }

    let Autores = await fetch(backendAddress + "artigos/autores/")
        .then(response => response.json()) as Autor[];
    
    let tbody = document.getElementById('idtbody') as HTMLTableSectionElement;
    tbody.innerHTML = ""
    for (let Autor of Autores) {
        let tr = document.createElement('tr') as HTMLTableRowElement;
        
        appendTextCell(tr, Autor.nome);
        
        let qtd = document.createElement('td') as HTMLTableCellElement;
        qtd.style.textAlign = "center";
        qtd.innerText = Autor.n_artigos.toString();
        tr.appendChild(qtd);
        
        // Ícones de ações:
        let tdAções = document.createElement('td') as HTMLTableCellElement;
        tdAções.style.textAlign = "center";

        let link = document.createElement('a') as HTMLAnchorElement;
        link.href = "listaArtigos.html?idAutor=" + Autor.id;
        let icon = document.createElement('img') as HTMLImageElement;
        icon.src = "images/view.png";
        icon.alt = "Ver textos deste autor";
        link.appendChild(icon);
        tdAções.appendChild(link);

        let edit = document.createElement('a') as HTMLAnchorElement; 
        edit.href = "atualizaAutor.html?id=" + Autor.id;
        let iconEdit = document.createElement('img') as HTMLImageElement;
        iconEdit.src = "images/edit.png";
        iconEdit.alt = "Editar o autor";
        edit.appendChild(iconEdit);
        tdAções.appendChild(edit);

        let deleteIcon = document.createElement('img') as HTMLImageElement;
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
            .catch(error => { console.log(error) })
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
