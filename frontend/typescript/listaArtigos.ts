onload = function () {
    (document.getElementById('insere') as HTMLButtonElement). 
        addEventListener('click', () => {location.href = 'insereArtigo.html'});
    (document.getElementById('remove') as HTMLButtonElement).
        addEventListener('click', removeArtigo);
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
            let autores = Artigo['autores']
                .map((autor: {id: number, nome: string}) => autor.nome)
                .join(', ');
            autores = (autores === "") ? "Sem autores cadastrados" : autores;

            appendTextCell(tr, Artigo['nome']);
            appendTextCell(tr, Artigo['ano_publicacao']);
            appendTextCell(tr, autores);
            
            tbody.appendChild(tr);
        }
    })
    .catch(error => {
        console.error("Erro:", error);
    });
}
