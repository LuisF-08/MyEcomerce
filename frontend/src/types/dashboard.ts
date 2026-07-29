export interface DashboardCards {
    faturamento: number
    pedidos_novos: number
    total_pedidos: number
    ticket_medio: number
}

export interface GraficoPedido {
    mes: string
    quantidade: number
    total: number
}

export interface ProdutoMaisVendido {
    id: number
    nome: string
    quantidade_vendida: number
}

export interface ItemPedido {
    produto_nome: string
    quantidade: number
}

export interface UltimoPedido {
    id: number
    cliente: string
    telefone?: string
    cidade?: string
    estado?: string
    total: number
    status: string
    criado_em: string
    itens?: ItemPedido[]
  }

export interface DashboardResponse {
    cards: DashboardCards
    grafico_pedidos: GraficoPedido[]
    produtos_mais_vendidos: ProdutoMaisVendido[]
    ultimos_pedidos: UltimoPedido[]
}
