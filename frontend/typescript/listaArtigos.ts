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
    fetch(backendAddress + "artigos/lista/")
    
    .then(response => response.json())
    
    .then(Artigos => {
        let campos = ['nome', 'ano_publicacao', 'autores', 'link'];
        let tbody = document.getElementById('idtbody') as HTMLTableSectionElement;
        tbody.innerHTML = ""
        for (let Artigo of Artigos) {
            let tr = document.createElement('tr') as HTMLTableRowElement;
            for (let i = 0; i < campos.length; i++) {
                let td = document.createElement('td') as HTMLTableCellElement;
                let href = document.createElement('a') as HTMLAnchorElement;
                href.setAttribute('href', 'update.html?id=' + Artigo['id']);
                let texto = document.createTextNode(Artigo[campos[i]]) as Text;
                href.appendChild(texto);
                td.appendChild(href);
                tr.appendChild(td);
            }
            let checkbox = document.createElement('input') as HTMLInputElement;
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('name', 'id');
            checkbox.setAttribute('value', Artigo['id']);
            let td = document.createElement('td') as HTMLTableCellElement;
            td.appendChild(checkbox);
            tr.appendChild(td);
            tbody.appendChild(tr);
        }
    })
    
    .catch(error => {
        console.error("Erro:", error);
    });
}
