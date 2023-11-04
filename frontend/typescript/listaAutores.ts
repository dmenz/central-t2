onload = function () {
    (document.getElementById('insere') as HTMLButtonElement). 
        addEventListener('click', () => {location.href = 'insereAutor.html'});
    (document.getElementById('remove') as HTMLButtonElement).
        addEventListener('click', remove);
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


function exibeListaDeAutores() {
    fetch(backendAddress + "autores/lista/")
    
    .then(response => response.json())
    
    .then(Autores => {
        let campos = ['nome'];
        let tbody = document.getElementById('idtbody') as HTMLTableSectionElement;
        tbody.innerHTML = ""
        for (let Autor of Autores) {
            let tr = document.createElement('tr') as HTMLTableRowElement;
            for (let i = 0; i < campos.length; i++) {
                let td = document.createElement('td') as HTMLTableCellElement;
                let href = document.createElement('a') as HTMLAnchorElement;
                href.setAttribute('href', 'update.html?id=' + Autor['id']);
                let texto = document.createTextNode(Autor[campos[i]]) as Text;
                href.appendChild(texto);
                td.appendChild(href);
                tr.appendChild(td);
            }
            let checkbox = document.createElement('input') as HTMLInputElement;
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('name', 'id');
            checkbox.setAttribute('value', Autor['id']);
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
