<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCarrinhoStore } from '@/stores/carrinho'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Empty from '@/components/common/Empty.vue'

const router = useRouter()
const carrinho = useCarrinhoStore()

const showModal = ref(false)
const nome = ref('')
const telefone = ref('')
const endereco = ref('')
const obs = ref('')

const preco = (v: number) => `R$ ${v.toFixed(2).replace('.', ',')}`

function enviarWhatsApp() {
  const itensTexto = carrinho.itens
    .map((i) => `• ${i.nome} x${i.qty} — ${preco(i.preco * i.qty)}`)
    .join('\n')

  const msg = encodeURIComponent(
    `Olá! Gostaria de fazer um pedido:\n\n${itensTexto}\n\nTotal: ${preco(carrinho.totalValor)}\n\nNome: ${nome.value}\nTelefone: ${telefone.value}${endereco.value ? `\nEndereço: ${endereco.value}` : ''}${obs.value ? `\nObs: ${obs.value}` : ''}`,
  )
  window.open(`https://wa.me/5511999999999?text=${msg}`, '_blank')
  carrinho.clear()
  showModal.value = false
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-zinc-900 mb-6">Seu carrinho</h1>

    <Empty
      v-if="!carrinho.itens.length"
      icon="pi pi-shopping-cart"
      title="Carrinho vazio"
      description="Adicione produtos ao carrinho para fazer seu pedido."
      action-label="Explorar produtos"
      @action="router.push({ name: 'categoria', params: { slug: 'todos' } })"
    />

    <div v-else class="flex flex-col md:flex-row gap-6">
      <!-- Items -->
      <div class="flex-1 space-y-4">
        <div
          v-for="item in carrinho.itens"
          :key="item.produtoId"
          class="bg-white border border-zinc-200 rounded-2xl p-4 flex items-center gap-4"
        >
          <div class="flex-1">
            <p class="text-sm font-semibold text-zinc-800">{{ item.nome }}</p>
            <p class="text-sm text-zinc-500">{{ preco(item.preco) }} cada</p>
          </div>
          <div class="flex items-center border border-zinc-200 rounded-xl overflow-hidden">
            <button
              class="px-3 py-1.5 text-zinc-600 hover:bg-zinc-100 font-bold"
              @click="carrinho.updateQty(item.produtoId, item.qty - 1)"
            >−</button>
            <span class="px-3 text-sm font-semibold min-w-8 text-center">{{ item.qty }}</span>
            <button
              class="px-3 py-1.5 text-zinc-600 hover:bg-zinc-100 font-bold"
              @click="carrinho.updateQty(item.produtoId, item.qty + 1)"
            >+</button>
          </div>
          <span class="text-sm font-bold text-zinc-900 w-24 text-right">{{ preco(item.preco * item.qty) }}</span>
          <button
            class="text-red-400 hover:text-red-600 transition-colors"
            @click="carrinho.removeItem(item.produtoId)"
          >
            <i class="pi pi-trash" />
          </button>
        </div>
      </div>

      <!-- Summary -->
      <div class="w-full md:w-72 shrink-0">
        <div class="bg-white border border-zinc-200 rounded-2xl p-6 sticky top-20">
          <h2 class="font-bold text-zinc-900 mb-4">Resumo do pedido</h2>
          <div class="space-y-2 mb-4">
            <div
              v-for="item in carrinho.itens"
              :key="item.produtoId"
              class="flex justify-between text-sm text-zinc-600"
            >
              <span class="truncate max-w-36">{{ item.nome }}</span>
              <span>{{ preco(item.preco * item.qty) }}</span>
            </div>
          </div>
          <div class="border-t border-zinc-100 pt-3 flex justify-between font-bold text-zinc-900 mb-5">
            <span>Total</span>
            <span class="text-orange-500">{{ preco(carrinho.totalValor) }}</span>
          </div>
          <button
            class="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2"
            @click="showModal = true"
          >
            <i class="pi pi-whatsapp" />
            Pedir pelo WhatsApp
          </button>
          <button
            class="w-full mt-2 text-sm text-zinc-500 hover:text-zinc-700 py-2 transition-colors"
            @click="carrinho.clear()"
          >
            Limpar carrinho
          </button>
        </div>
      </div>
    </div>

    <!-- WhatsApp Dialog -->
    <Dialog
      v-model:visible="showModal"
      header="Finalizar pedido"
      :modal="true"
      :style="{ width: '460px' }"
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
        <button
          class="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-xl transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
          :disabled="!nome || !telefone"
          @click="enviarWhatsApp"
        >
          <i class="pi pi-whatsapp" />
          Enviar pedido pelo WhatsApp
        </button>
      </template>
    </Dialog>
  </div>
</template>
