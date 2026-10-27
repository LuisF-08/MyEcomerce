import { ref } from 'vue'

import { useCarrinhoStore } from '@/stores/carrinho'
import { criarCheckout, criarPagamento } from '@/services/pagamento'

export interface DadosCliente {
    nome: string
    telefone: string
    endereco?: string
    observacao?: string
}

/**
 * Lógica do pagamento online, reutilizável em qualquer componente.
 *
 * Uso:
 *   const { carregando, erro, pagarMercadoPago } = usePagamento()
 *   await pagarMercadoPago({ nome, telefone })
 */
export function usePagamento() {
    const carrinho = useCarrinhoStore()

    const carregando = ref(false)
    const erro = ref('')

    async function pagarMercadoPago(cliente: DadosCliente) {
        if (carregando.value) return
    
        if (!carrinho.itens.length) {
            erro.value = 'Seu carrinho está vazio.'
            return
        }
    
        carregando.value = true
        erro.value = ''
    
        try {
            // Cria o pedido. Só mandamos produto e quantidade: o preço vem do banco.
            const pedido = await criarCheckout({
                nome: cliente.nome.trim(),
                telefone: cliente.telefone.trim(),
                rua: cliente.endereco?.trim() ?? '',
                observacao: cliente.observacao?.trim() ?? '',
                itens: carrinho.itens.map((item) => ({
                    produto: item.produtoId,
                    quantidade: item.quantidade,
                    ...(item.variacao ? { variacao: item.variacao } : {}),
                })),
            })

            // Guarda os dados do cliente para montar a mensagem do WhatsApp na volta
            localStorage.setItem(
                'pedido_pendente',
                JSON.stringify({
                    id: pedido.id,
                    nome: cliente.nome.trim(),
                    telefone: cliente.telefone.trim(),
                    endereco: cliente.endereco?.trim() ?? '',
                    observacao: cliente.observacao?.trim() ?? '',
                }),
            )

            // Gera o link de pagamento desse pedido
            const pagamento = await criarPagamento(pedido.id)

            // Vai para o Mercado Pago. O carrinho NÃO é limpo aqui:
            // isso só acontece na tela de retorno, quando o backend confirmar.
            window.location.href = pagamento.init_point
        } catch {
            erro.value = 'Não foi possível iniciar o pagamento. Tente novamente.'
            carregando.value = false
        }
        // Em caso de sucesso, 'carregando' continua true de propósito:
        // o navegador está saindo da página.
    }

    return { carregando, erro, pagarMercadoPago }
}