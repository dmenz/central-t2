onload = function () {
    exibeListaDeArtigos(); // exibe lista de Artigos ao carregar a página
}


const removeArtigo = () => {
    let idArray =  [];
    let checkboxes = document.getElementsByTagName('input');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            idArray.push(checkboxes[i].value)
        }
    }
    fetch(backendAddress + 'artigos/lista/', {
        method: 'DELETE', 
        headers: {
            'Authorization': tokenKeyword + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(idArray)
    })
    .then(response => { exibeListaDeArtigos() })
    .catch(error => { console.log(error) })
}


function exibeListaDeArtigos() {
    const appendTextCell = (tr: HTMLTableRowElement, text: string) => {
        let td = document.createElement('td') as HTMLTableCellElement;
        td.appendChild(document.createTextNode(text));
        tr.appendChild(td);
    }

    fetch(backendAddress + "artigos/artigos/")
    
    .then(response => response.json())
    
    .then(Artigos => {
        let tbody = document.getElementById('idtbody') as HTMLTableSectionElement;
        tbody.innerHTML = ""
        for (let Artigo of Artigos) {
            let tr = document.createElement('tr') as HTMLTableRowElement;

            appendTextCell(tr, Artigo.nome);
            appendTextCell(tr, Artigo.ano_publicacao);

            let autores = Artigo.autores
                .map((autor: {id: number, nome: string}) => autor.nome)
                .join('; ');
            if (autores === "")
                autores = "Sem autores cadastrados";
            appendTextCell(tr, autores);

            // Ícones de ações:
            let tdAções = document.createElement('td') as HTMLTableCellElement;
            tdAções.style.textAlign = "center";

            let link = document.createElement('a') as HTMLAnchorElement;
            link.href = Artigo.link;
            link.target = "_blank";
            if (Artigo.link === null || Artigo.link === "" || Artigo.link === undefined)
                link.style.visibility = "hidden";
            let icon = document.createElement('img') as HTMLImageElement;
            icon.src = "images/view.png";
            icon.alt = "Visitar o artigo";
            link.appendChild(icon);
            tdAções.appendChild(link);

            let edit = document.createElement('a') as HTMLAnchorElement; 
            edit.href = "insereArtigo.html?id=" + Artigo.id;
            let iconEdit = document.createElement('img') as HTMLImageElement;
            iconEdit.src = "images/edit.png";
            iconEdit.alt = "Editar o artigo";
            edit.appendChild(iconEdit);
            tdAções.appendChild(edit);

            // Esse ícone ficou como parágrafo porque o clique nele não leva
            // para outra página, e ajudou na hora de alinhar os ícones numa
            // mesma linha.
            let del = document.createElement('p') as HTMLParagraphElement;
            del.style.display = "inline";
            let deleteIcon = document.createElement('img') as HTMLImageElement;
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
                .then(response => { exibeListaDeArtigos() })
                .catch(error => { console.log(error) })
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
