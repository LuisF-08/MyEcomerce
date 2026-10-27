import type { PedidoConfirmado } from '@/types/pagamento'

export interface DadosEntrega {
  nome?: string
  telefone?: string
  endereco?: string
  observacao?: string
}

const brl = (v: number | string) =>
  Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

export function montarMensagemPedidoPago(
  pedido: PedidoConfirmado,
  cliente: DadosEntrega | null,
  paymentId: string,
): string {
  const codigo = `#${String(pedido.id).padStart(4, '0')}`

  const itens = pedido.itens
    .map(
      (i) =>
        `• ${i.produto_nome}${i.variacao ? ` (${i.variacao})` : ''} x${i.quantidade} — ${brl(i.subtotal)}`,
    )
    .join('\n')

  const linhas = [
    `Olá! Acabei de pagar o pedido ${codigo} pelo site ✅`,
    '',
    itens,
    '',
    `Total pago: ${brl(pedido.total)}`,
    `Pagamento: Mercado Pago (aprovado) · ID ${paymentId}`,
  ]

  if (cliente?.nome) linhas.push('', `Nome: ${cliente.nome}`)
  if (cliente?.telefone) linhas.push(`Telefone: ${cliente.telefone}`)
  if (cliente?.endereco) linhas.push(`Endereço: ${cliente.endereco}`)
  if (cliente?.observacao) linhas.push(`Obs: ${cliente.observacao}`)

  return linhas.join('\n')
}