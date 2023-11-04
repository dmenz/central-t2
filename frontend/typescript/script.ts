onload = function () {
    (document.getElementById('insere') as HTMLButtonElement). 
        addEventListener('click', () => {location.href = 'insereCarro.html'});
    (document.getElementById('remove') as HTMLButtonElement).
        addEventListener('click', remove);
    exibeListaDeCarros(); // exibe lista de carros ao carregar a página
}

const remove = () => {
    let idArray =  [];
    let checkboxes = document.getElementsByTagName('input');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            idArray.push(checkboxes[i].value)
        }
    }
    fetch(backendAddress + 'carros/lista/', {
        method: 'DELETE', 
        headers: {
            'Authorization': tokenKeyword + localStorage.getItem('token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(idArray)
    })
    .then(response => { exibeListaDeCarros() })
    .catch(error => { console.log(error) })
}

function exibeListaDeCarros() {
    fetch(backendAddress + "carros/lista/")
    .then(response => response.json())
    .then(carros => {
        let campos = ['name', 'mpg', 'cyl', 'disp', 'hp', 'drat',
                      'wt', 'qsec', 'vs', 'am', 'gear', 'carb'];
        let tbody = document.getElementById('idtbody') as HTMLTableSectionElement;
        tbody.innerHTML = ""
        for (let carro of carros) {
            let tr = document.createElement('tr') as HTMLTableRowElement;
            for (let i = 0; i < campos.length; i++) {
                let td = document.createElement('td') as HTMLTableCellElement;
                let href = document.createElement('a') as HTMLAnchorElement;
                href.setAttribute('href', 'update.html?id=' + carro['id']);
                let texto = document.createTextNode(carro[campos[i]]) as Text;
                href.appendChild(texto);
                td.appendChild(href);
                tr.appendChild(td);
            }
            let checkbox = document.createElement('input') as HTMLInputElement;
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('name', 'id');
            checkbox.setAttribute('value', carro['id']);
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
