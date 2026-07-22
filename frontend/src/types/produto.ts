export interface Produto {
    id:number
    nome:string
    descricao:string
    preco:number
    quantidade:number
    categoria:number
    categoria_nome:string
    imagem_1:string | null
    imagem_2:string | null
    ativo:boolean
    destaque:boolean
}