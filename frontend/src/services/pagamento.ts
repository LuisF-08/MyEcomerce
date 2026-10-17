import type { CheckoutPayload, CheckoutResposta 
    , CriarPagamentoResposta,ConfirmarPagamentoResposta
} from '@/types/pagamento'
import api from '@/api/api'

export async function criarCheckout(dados: CheckoutPayload
    ): Promise<CheckoutResposta> {
        const response = await api.post<CheckoutResposta>('/checkout/', dados)
        return response.data
}

export async function criarPagamento(
    solicitacaoId: number): Promise<CriarPagamentoResposta> {
        const response = await api.post<CriarPagamentoResposta>(
            '/pagamentos/criar/',
            { solicitacao: solicitacaoId}
        )
        return response.data
}

export async function confirmarPagamento(
    paymentId: string
): Promise<ConfirmarPagamentoResposta> {
    const response = await api.post<ConfirmarPagamentoResposta>(
        '/pagamentos/confirmar/',
        { payment_id: paymentId}
    )
    return response.data
}