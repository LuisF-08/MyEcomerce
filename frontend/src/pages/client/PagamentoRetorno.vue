<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import { confirmarPagamento } from '@/services/pagamento'
import { useCarrinhoStore } from '@/stores/carrinho'
import { useLojaStore } from '@/stores/loja'
import { whatsappLink } from '@/utils/loja'
import { montarMensagemPedidoPago, type DadosEntrega } from '@/utils/pedido'
import type { PedidoConfirmado, StatusPagamento } from '@/types/pagamento'

type Estado = 'carregando' | StatusPagamento | 'erro'

const route = useRoute()
const router = useRouter()
const carrinho = useCarrinhoStore()
const lojaStore = useLojaStore()
const { loja } = storeToRefs(lojaStore)

const estado = ref<Estado>('carregando')
const pedido = ref<PedidoConfirmado | null>(null)
const paymentId = ref('')
const segundos = ref(0)
let timer: ReturnType<typeof setInterval> | undefined

// Dados do cliente salvos antes de ir ao Mercado Pago (lidos uma vez)
function lerSnapshot(): (DadosEntrega & { id?: number }) | null {
  try {
    return JSON.parse(localStorage.getItem('pedido_pendente') || 'null')
  } catch {
    return null
  }
}
const snapshot = lerSnapshot()

const linkWhatsapp = computed(() => {
  if (!pedido.value) return '#'
  const cliente = snapshot && snapshot.id === pedido.value.id ? snapshot : null
  const mensagem = montarMensagemPedidoPago(pedido.value, cliente, paymentId.value)
  return whatsappLink(loja.value, mensagem)
})

const chaveEnviado = computed(() => `wpp_enviado_${pedido.value?.id}`)

function cancelar() {
  clearInterval(timer)
  segundos.value = 0
}

function enviar() {
  cancelar()
  if (!pedido.value || linkWhatsapp.value === '#') return
  localStorage.setItem(chaveEnviado.value, '1')
  localStorage.removeItem('pedido_pendente')
  window.location.href = linkWhatsapp.value
}

function iniciarContagem() {
  if (localStorage.getItem(chaveEnviado.value)) return // já enviado antes
  if (linkWhatsapp.value === '#') return
  segundos.value = 5
  timer = setInterval(() => {
    segundos.value--
    if (segundos.value <= 0) enviar()
  }, 1000)
}

onMounted(async () => {
  const bruto = route.query.payment_id ?? route.query.collection_id
  paymentId.value = String((Array.isArray(bruto) ? bruto[0] : bruto) ?? '')

  if (!/^\d{1,20}$/.test(paymentId.value)) {
    estado.value = 'erro'
    return
  }

  try {
    const r = await confirmarPagamento(paymentId.value)
    estado.value = r.status

    if (r.status === 'aprovado' && r.pedido) {
      pedido.value = r.pedido
      carrinho.limpar()
      await lojaStore.carregarLoja() // garante o número de WhatsApp
      iniciarContagem()
    }
  } catch {
    estado.value = 'erro'
  }
})

onUnmounted(() => clearInterval(timer))

const visual = computed(() => {
  switch (estado.value) {
    case 'aprovado':
      return { icon: 'pi pi-check-circle', cor: 'text-emerald-500', bg: 'bg-emerald-50 dark:bg-emerald-500/10',
        titulo: 'Pagamento aprovado!', texto: 'Recebemos o seu pedido. Obrigado pela compra!' }
    case 'pendente':
      return { icon: 'pi pi-clock', cor: 'text-amber-500', bg: 'bg-amber-50 dark:bg-amber-500/10',
        titulo: 'Pagamento pendente', texto: 'Estamos aguardando a confirmação. Assim que for aprovado, seu pedido entra na fila.' }
    case 'recusado':
      return { icon: 'pi pi-times-circle', cor: 'text-red-500', bg: 'bg-red-50 dark:bg-red-500/10',
        titulo: 'Pagamento recusado', texto: 'O pagamento não foi aprovado. Seu carrinho continua salvo, tente novamente.' }
    case 'cancelado':
      return { icon: 'pi pi-ban', cor: 'text-zinc-500', bg: 'bg-zinc-100 dark:bg-zinc-800',
        titulo: 'Pagamento cancelado', texto: 'O pagamento foi cancelado. Seu carrinho continua salvo.' }
    case 'estornado':
      return { icon: 'pi pi-replay', cor: 'text-blue-500', bg: 'bg-blue-50 dark:bg-blue-500/10',
        titulo: 'Pagamento estornado', texto: 'O valor foi devolvido.' }
    case 'erro':
      return { icon: 'pi pi-exclamation-triangle', cor: 'text-red-500', bg: 'bg-red-50 dark:bg-red-500/10',
        titulo: 'Não foi possível confirmar', texto: 'Não conseguimos confirmar o pagamento. Se você já pagou, fale com a loja informando seu nome e telefone.' }
    default:
      return { icon: 'pi pi-spin pi-spinner', cor: 'text-orange-500', bg: 'bg-orange-50 dark:bg-orange-500/10',
        titulo: 'Confirmando pagamento...', texto: 'Aguarde enquanto confirmamos os detalhes do seu pedido.' }
  }
})
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-16 sm:py-24 text-center">
    <div :class="['w-20 h-20 rounded-full mx-auto flex items-center justify-center mb-6', visual.bg]">
      <i :class="[visual.icon, visual.cor, 'text-4xl']" />
    </div>

    <h1 class="text-2xl font-extrabold text-zinc-900 dark:text-white mb-2">{{ visual.titulo }}</h1>
    <p class="text-zinc-500 dark:text-zinc-400 text-sm leading-relaxed">{{ visual.texto }}</p>

    <p v-if="pedido" class="mt-3 text-xs font-mono text-zinc-400">
      Pedido #{{ String(pedido.id).padStart(4, '0') }}
    </p>

    <!-- Envio do pedido para o WhatsApp da loja -->
    <div
      v-if="estado === 'aprovado' && pedido"
      class="mt-6 rounded-2xl border border-green-200 dark:border-green-500/20 bg-green-50 dark:bg-green-500/10 p-4 text-left"
    >
      <p class="text-sm font-semibold text-green-800 dark:text-green-300 flex items-center gap-2">
        <i class="pi pi-whatsapp" /> Envie o pedido para a loja
      </p>
      <p class="text-xs text-green-700/80 dark:text-green-300/70 mt-1">
        Vamos abrir o WhatsApp com os detalhes da compra já preenchidos.
      </p>
      <p v-if="segundos > 0" class="text-xs font-semibold text-green-800 dark:text-green-300 mt-2">
        Abrindo em {{ segundos }}s...
      </p>

      <div class="flex flex-col sm:flex-row gap-2 mt-3">
        <button
          type="button"
          class="flex-1 px-4 py-2.5 rounded-xl bg-green-500 hover:bg-green-600 text-white text-sm font-semibold transition-colors"
          @click="enviar"
        >
          <i class="pi pi-whatsapp mr-1" /> {{ segundos > 0 ? 'Enviar agora' : 'Enviar pedido no WhatsApp' }}
        </button>
        <button
          v-if="segundos > 0"
          type="button"
          class="px-4 py-2.5 rounded-xl border border-green-300 dark:border-green-500/30 text-green-800 dark:text-green-300 text-sm font-semibold hover:bg-green-100 dark:hover:bg-green-500/10 transition-colors"
          @click="cancelar"
        >
          Cancelar
        </button>
      </div>
    </div>

    <div v-if="estado !== 'carregando'" class="mt-8 flex flex-col sm:flex-row gap-3 justify-center">
      <button
        class="px-6 py-3 rounded-xl bg-orange-500 hover:bg-orange-600 text-white font-semibold transition-colors"
        @click="router.push({ name: 'home' })"
      >
        Voltar à loja
      </button>
      <button
        v-if="['recusado', 'cancelado', 'pendente', 'erro'].includes(estado)"
        class="px-6 py-3 rounded-xl border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-200 font-semibold hover:bg-zinc-50 dark:hover:bg-zinc-800 transition-colors"
        @click="carrinho.abrir(); router.push({ name: 'home' })"
      >
        Ver carrinho
      </button>
    </div>
  </div>
</template>