// ---------- Checkout (cria o pedido) ----------

export interface ItemCheckout {
    produto: number
    quantidade: number
    variacao?: string
}

export interface CheckoutPayload {
    nome: string
    telefone: string
    rua?: string
    observacao?: string
    itens: ItemCheckout[]
}

export interface CheckoutResposta {
    id: number
    total: string
    status: string
}

// ---------- Pagamento ----------

export type StatusPagamento =
    | 'pendente'
    | 'aprovado'
    | 'recusado'
    | 'cancelado'
    | 'estornado'

// Resposta de POST /pagamentos/criar/
export interface CriarPagamentoResposta {
    pagamento_id: number
    init_point: string
}

export interface ItemPedidoConfirmado {
    produto_nome: string
    quantidade: number
    variacao: string
    subtotal: string
}

export interface PedidoConfirmado {
    id: number
    total: string
    itens: ItemPedidoConfirmado[]
}

// Resposta de POST /pagamentos/confirmar/
export interface ConfirmarPagamentoResposta {
    status: StatusPagamento
    solicitacao: number
    pedido?: PedidoConfirmado
}