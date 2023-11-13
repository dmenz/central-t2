onload = function () {
    let buscar = document.getElementById('buscar') as HTMLInputElement;
    buscar.addEventListener('click', exibeListaDeArtigos);

    let urlParams = new URLSearchParams(window.location.search);
    let idAutor = urlParams.get('idAutor') as string;
    let nomeAutor = document.getElementById('autor-escolhido') as HTMLSpanElement;
    if (idAutor !== null && idAutor !== "")
        fetch(backendAddress + 'artigos/autor/' + idAutor)
        .then(response => response.json())
        .then( (autor: Autor) =>  nomeAutor.innerText = " de " + autor.nome );
    else {
        nomeAutor.innerText = "";
    }

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
    .then(_ => exibeListaDeArtigos() )
    .catch(error => { console.log(error) })
}


function exibeListaDeArtigos() {
    const appendTextCell = (tr: HTMLTableRowElement, text: string) => {
        let td = document.createElement('td') as HTMLTableCellElement;
        td.appendChild(document.createTextNode(text));
        tr.appendChild(td);
    }

    let titulo = document.getElementsByName('titulo')[0] as HTMLInputElement;
    let autor = document.getElementsByName('autor')[0] as HTMLInputElement;
    const queryString = new URLSearchParams({
        titulo: titulo.value || "",
        autor: autor.value || ""
    }).toString();

    fetch(backendAddress + "artigos/artigos/?" + queryString)
    
    .then(response => response.json())
    
    .then( (artigos:Artigo[]) => {
        let tbody = document.getElementById('idtbody') as HTMLTableSectionElement;
        tbody.innerHTML = ""

         // se a página foi aberta a partir de um autor
        let urlParams = new URLSearchParams(window.location.search);
        let idAutor = urlParams.get('idAutor') as string;
        if (idAutor !== null || idAutor === "") {
            artigos = artigos.filter(at =>
                         at.autores.some( au => au.id === parseInt(idAutor) )
                    );
        }
        if (artigos.length === 0) {
            let tr = document.createElement('tr') as HTMLTableRowElement;
            let td = document.createElement('td') as HTMLTableCellElement;
            td.colSpan = 4;
            td.style.textAlign = "center";
            td.innerText = "Sem resultados";
            tr.appendChild(td);
            tbody.appendChild(tr);
        }
        else for (let Artigo of artigos) {
            let tr = document.createElement('tr') as HTMLTableRowElement;

            appendTextCell(tr, Artigo.nome);
            appendTextCell(tr, Artigo.ano_publicacao.toString());

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
            edit.href = "atualizaArtigo.html?id=" + Artigo.id;
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
