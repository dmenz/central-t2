onload = async() => {
    let todosAutores = await fetch(backendAddress + 'artigos/autores/',
            { method: 'GET', headers: {'Content-Type': 'application/json'}})
        .then(response => response.json()) as Autor[];
    
    let select = document.getElementById('autores') as HTMLSelectElement;
    for (let autor of todosAutores) {
        let option = document.createElement('option') as HTMLOptionElement;
        option.value = autor.id.toString();
        option.text = autor.nome;
        select.add(option);
    }

    (document.getElementById('insere') as HTMLButtonElement).addEventListener('click', evento => {
        evento.preventDefault();
        
        // pega todos os elementos do formulário
        const elements = (document.getElementById('meuFormulario') as HTMLFormElement).elements;
        
        // dicionário vazio
        let data: Record<string, any> = {};
        // preenche o dicionário com os pares nome/valor
        for (let i = 0; i < elements.length; i++) {
            const element = elements[i] as HTMLInputElement | HTMLSelectElement;
            if (element.name == 'autores') {
                let select = element as HTMLSelectElement;
                let selectedOptions = Array.from(select.selectedOptions);
                data[element.name] = selectedOptions.map(o => parseInt(o.value));
            } else {
                data[element.name] = element.value;
            }
        }
        
        // envia os dados para o backend
        fetch(backendAddress + "artigos/artigo/", {
                method: 'POST', 
                headers: {
                    'Authorization': tokenKeyword + localStorage.getItem('token'),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
        
        .then(response => {
                let lugar = (document.getElementById('mensagem') as HTMLDivElement)
                if(response.ok) {
                    lugar.innerHTML = 'Dados de artigo inseridos com sucesso';
                } else {
                    lugar.innerHTML = 'Dados de artigo com erro';
                }
            }
        )
        
        .catch(error => { console.log(error) })
    });
}
