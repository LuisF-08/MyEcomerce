interface ItemSolicitacao {
  id?: number
  solicitacao?: number
  produto: number
  produto_nome?: string
  preco_unitario?: number | string
  quantidade: number
  subtotal?: number | string
  variacao?: string
  criado_em?: string
}

export interface Solicitacao {
  id: number
  nome: string
  telefone: string
  email: string
  cep: string
  rua: string
  numero: string
  referencia: string
  bairro: string
  cidade: string
  estado: string
  observacao: string
  total: number | string
  mensagem: string
  status: string
  itens: ItemSolicitacao[]
  criado_em: string
}

