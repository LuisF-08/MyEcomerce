export interface ItemCarrinho {
    produtoId: number
    nome: string
    preco: number
    imagem: string | null
    quantidade: number
    variacao?: string
}