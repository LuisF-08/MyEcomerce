export interface Categoria {
    id: number
    nome: string
    descricao: string
    imagem: string | null
    ativo: boolean
    ordem: number
}