<script setup lang="ts">
import { ref } from 'vue'
import { useCarrinhoStore } from '@/stores/carrinho'
import Drawer from 'primevue/drawer'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'

const carrinho = useCarrinhoStore()

const showModal = ref(false)
const nome = ref('')
const telefone = ref('')
const endereco = ref('')
const obs = ref('')

const preco = (v: number) =>
    v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

function enviarWhatsApp() {
  const itensTexto = carrinho.itens
    .map((i) => `• ${i.nome} x${i.quantidade} — ${preco(i.preco * i.quantidade)}`)
    .join('\n')

  const msg = encodeURIComponent(
    `Olá! Gostaria de fazer um pedido:\n\n${itensTexto}\n\nTotal: ${preco(carrinho.valorTotal)}\n\nNome: ${nome.value}\nTelefone: ${telefone.value}${endereco.value ? `\nEndereço: ${endereco.value}` : ''}${obs.value ? `\nObs: ${obs.value}` : ''}`,
  )
  window.open(`https://wa.me/5511999999999?text=${msg}`, '_blank')
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
    class="!w-full sm:!w-96"
  >
    <div v-if="!carrinho.itens.length" class="flex flex-col items-center justify-center h-full text-center gap-3 text-zinc-400">
      <i class="pi pi-shopping-cart text-4xl" />
      <p class="text-sm">Seu carrinho está vazio</p>
    </div>

    <div v-else class="flex flex-col h-full">
      <!-- Lista -->
      <div class="flex-1 overflow-y-auto space-y-3 pr-1">
        <div
          v-for="item in carrinho.itens"
          :key="item.produtoId"
          class="border border-zinc-200 rounded-2xl p-3 flex items-center gap-3"
        >
          <img
            v-if="item.imagem"
            :src="item.imagem"
            :alt="item.nome"
            class="w-14 h-14 object-cover rounded-xl shrink-0"
          >
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold text-zinc-800 truncate">{{ item.nome }}</p>
            <p class="text-xs text-zinc-500">{{ preco(item.preco) }} cada</p>

            <div class="flex items-center gap-2 mt-1">
              <button
                class="w-6 h-6 flex items-center justify-center rounded-full border border-zinc-200 text-zinc-600 hover:bg-zinc-100"
                @click="carrinho.diminuir(item.produtoId)"
              >−</button>
              <span class="text-sm font-semibold min-w-4 text-center">{{ item.quantidade }}</span>
              <button
                class="w-6 h-6 flex items-center justify-center rounded-full border border-zinc-200 text-zinc-600 hover:bg-zinc-100"
                @click="carrinho.incrementar(item.produtoId)"
              >+</button>
            </div>
          </div>

          <div class="flex flex-col items-end gap-2">
            <span class="text-sm font-bold text-zinc-900">{{ preco(item.preco * item.quantidade) }}</span>
            <button
              class="text-red-400 hover:text-red-600 transition-colors"
              @click="carrinho.removerItem(item.produtoId)"
            >
              <i class="pi pi-trash text-sm" />
            </button>
          </div>
        </div>
      </div>

      <!-- Resumo -->
      <div class="border-t border-zinc-100 pt-4 mt-4 shrink-0">
        <div class="flex justify-between font-bold text-zinc-900 mb-4">
          <span>Total</span>
          <span class="text-orange-500">{{ preco(carrinho.valorTotal) }}</span>
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
          @click="carrinho.limpar()"
        >
          Limpar carrinho
        </button>
      </div>
    </div>
  </Drawer>

  <!-- Modal do formulário WhatsApp -->
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
</template>