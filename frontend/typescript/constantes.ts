type Autor = {
    id: number,
    nome: string,
    n_artigos: number
};

type Artigo = {
    id: number,
    nome: string,
    ano_publicacao: number,
    link: string,
    autores: Autor[],
};

const backendAddress = window.location.protocol + '//' +
                        window.location.hostname + ':8000/'

const tokenKeyword = 'Token '

