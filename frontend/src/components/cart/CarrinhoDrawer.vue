<script setup lang="ts">
import { ref } from 'vue'
import { useCarrinhoStore } from '@/stores/carrinho'
import { usePagamento } from '../controller/usePagamento.ts'
import Drawer from 'primevue/drawer'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import ImagemComFallback from '../ui/ImagemComFallback.vue'

const carrinho = useCarrinhoStore()

const showModal = ref(false)
const nome = ref('')
const telefone = ref('')
const endereco = ref('')
const obs = ref('')

// O mesmo modal serve para WhatsApp e para Mercado Pago
type Modo = 'whatsapp' | 'mercadopago'
const modo = ref<Modo>('whatsapp')

// Estado e ação do pagamento vêm do composable
const {
  carregando: carregandoMp,
  erro,
  pagarMercadoPago: iniciarPagamento,
} = usePagamento()

function abrirModal(m: Modo) {
  modo.value = m
  erro.value = ''
  showModal.value = true
}

function pagarMercadoPago() {
  iniciarPagamento({
    nome: nome.value,
    telefone: telefone.value,
    endereco: endereco.value,
    observacao: obs.value,
  })
}

const preco = (v: number) =>
  v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

function enviarWhatsApp() {
  const itensTexto = carrinho.itens
    .map((i) => `• ${i.nome} x${i.quantidade} — ${preco(i.preco * i.quantidade)}`)
    .join('\n')

  const msg = encodeURIComponent(
    `Olá! Gostaria de fazer um pedido:\n\n${itensTexto}\n\nTotal: ${preco(carrinho.valorTotal)}\n\nNome: ${nome.value}\nTelefone: ${telefone.value}${endereco.value ? `\nEndereço: ${endereco.value}` : ''}${obs.value ? `\nObs: ${obs.value}` : ''}`,
  )
  window.open(`https://wa.me/55999081860?text=${msg}`, '_blank')
  carrinho.limpar()
  showModal.value = false
  carrinho.fechar()
}
</script>

<template>
  <Drawer
    v-model:visible="carrinho.aberto"
    header="Seu carrinho"
    position="right"
    class="drawer-carrinho"
    :pt="{ content: { class: 'flex flex-col min-h-0' } }"
  >
    <!-- Vazio -->
    <div
      v-if="!carrinho.itens.length"
      class="flex-1 flex flex-col items-center justify-center text-center gap-3 text-zinc-400"
    >
      <i class="pi pi-shopping-cart text-4xl" />
      <p class="text-sm">Seu carrinho está vazio</p>
    </div>

    <div v-else class="flex-1 min-h-0 flex flex-col">
      <!-- Lista (rola sozinha, o resumo fica sempre visível embaixo) -->
      <div class="lista-itens flex-1 min-h-0 overflow-y-auto space-y-4">
        <div
          v-for="item in carrinho.itens"
          :key="item.produtoId"
          class="border border-zinc-200 rounded-2xl p-4 flex flex-col gap-4"
        >
          <!-- Produto -->
          <div class="flex items-center gap-4 min-w-0">
            <ImagemComFallback
              :src="item.imagem"
              :alt="item.nome"
              aspect=""
              class="w-16 h-16 rounded-xl shrink-0"
            />
            <div class="min-w-0">
              <p class="text-sm font-semibold text-zinc-800 break-words">{{ item.nome }}</p>
              <p class="text-xs text-zinc-500">{{ preco(item.preco) }} cada</p>
            </div>
          </div>

          <!-- Ações -->
          <div class="flex items-center justify-between gap-3 pt-3 border-t border-zinc-100">
            <div class="flex items-center gap-2">
              <button
                type="button"
                aria-label="Diminuir quantidade"
                class="w-8 h-8 shrink-0 flex items-center justify-center rounded-full border border-zinc-200 text-zinc-600 hover:bg-zinc-100 active:bg-zinc-200"
                @click.stop="carrinho.diminuir(item.produtoId)"
              >−</button>
              <span class="text-sm font-semibold w-6 text-center">{{ item.quantidade }}</span>
              <button
                type="button"
                aria-label="Aumentar quantidade"
                class="w-8 h-8 shrink-0 flex items-center justify-center rounded-full border border-zinc-200 text-zinc-600 hover:bg-zinc-100 active:bg-zinc-200"
                @click.stop="carrinho.incrementar(item.produtoId)"
              >+</button>
            </div>

            <div class="flex items-center gap-2">
              <span class="text-sm font-bold text-zinc-900 text-right">
                {{ preco(item.preco * item.quantidade) }}
              </span>
              <button
                type="button"
                aria-label="Remover item"
                class="w-8 h-8 shrink-0 flex items-center justify-center text-red-400 hover:text-red-600 transition-colors"
                @click.stop="carrinho.removerItem(item.produtoId)"
              >
                <i class="pi pi-trash text-sm" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumo -->
      <div class="border-t border-zinc-100 pt-4 mt-4 shrink-0">
        <div class="flex justify-between font-bold text-zinc-900 mb-4">
          <span>Total</span>
          <span class="text-orange-500">{{ preco(carrinho.valorTotal) }}</span>
        </div>

        <!-- Botão WhatsApp -->
        <button
          type="button"
          class="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
          @click="abrirModal('whatsapp')"
        >
          <i class="pi pi-whatsapp" />
          Pedir pelo WhatsApp
        </button>

        <!-- Botão Mercado Pago -->
        <button
          type="button"
          class="w-full mt-2 bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
          @click="abrirModal('mercadopago')"
        >
          <i class="pi pi-credit-card" />
          Pagar com Mercado Pago
        </button>

        <button
          type="button"
          class="w-full mt-2 text-sm text-zinc-500 hover:text-zinc-700 py-2 transition-colors"
          @click="carrinho.limpar()"
        >
          Limpar carrinho
        </button>
      </div>
    </div>
  </Drawer>

  <!-- Modal do formulário (WhatsApp e Mercado Pago) -->
  <Dialog
    v-model:visible="showModal"
    header="Finalizar pedido"
    :modal="true"
    :style="{ width: '460px', maxWidth: '95vw' }"
  >
    <div class="space-y-4 py-2">
      <div>
        <label class="text-xs font-semibold text-zinc-600 mb-1 block">Seu nome *</label>
        <InputText v-model="nome" placeholder="Ex: Maria Silva" class="w-full" />
      </div>
      <div>
        <label class="text-xs font-semibold text-zinc-600 mb-1 block">WhatsApp *</label>
        <InputText v-model="telefone" placeholder="(11) 9 9999-9999" class="w-full" />
      </div>
      <div>
        <label class="text-xs font-semibold text-zinc-600 mb-1 block">Endereço (opcional)</label>
        <InputText v-model="endereco" placeholder="Rua, número, bairro" class="w-full" />
      </div>
      <div>
        <label class="text-xs font-semibold text-zinc-600 mb-1 block">Observações (opcional)</label>
        <Textarea v-model="obs" rows="2" placeholder="Tamanho, cor, instruções..." class="w-full" />
      </div>
    </div>

    <template #footer>
      <p v-if="erro" class="text-sm text-red-500 mb-3 text-left w-full">{{ erro }}</p>

      <button
        v-if="modo === 'whatsapp'"
        type="button"
        class="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
        :disabled="!nome || !telefone"
        @click="enviarWhatsApp"
      >
        <i class="pi pi-whatsapp" />
        Enviar pedido pelo WhatsApp
      </button>

      <button
        v-else
        type="button"
        class="w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
        :disabled="!nome || !telefone || carregandoMp"
        @click="pagarMercadoPago"
      >
        <i :class="carregandoMp ? 'pi pi-spinner pi-spin' : 'pi pi-credit-card'" />
        {{ carregandoMp ? 'Gerando pagamento...' : 'Ir para o pagamento' }}
      </button>
    </template>
  </Dialog>
</template>

<style scoped>
/* Mantém a rolagem, mas esconde a barra */
.lista-itens {
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.lista-itens::-webkit-scrollbar {
  display: none;
}
</style>

<style>
/* Largura do Drawer: tela cheia no mobile, painel largo no desktop */
.drawer-carrinho {
  width: 100% !important;
}
@media (min-width: 768px) {
  .drawer-carrinho {
    width: 34rem !important;
    max-width: 90vw;
  }
}
</style>