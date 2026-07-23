<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'

import { useProdutosStore } from '@/stores/produto'
import { useCarrinhoStore } from '@/stores/carrinho'
import type { Produto } from '@/types/produto'

import ProdutoCard from '@/components/catalogo/ProdutoCard.vue'
import Empty from '@/components/common/Empty.vue'
import Loading from '@/components/common/Loading.vue'

const route = useRoute()
const produtoStore = useProdutosStore()
const carrinho = useCarrinhoStore()
const toast = useToast()

const produto = ref<Produto | null>(null)
const imgAtiva = ref(0)
const qty = ref(1)

// Imagem placeholder padrão em SVG caso o produto não tenha imagem ou a URL falhe
const PLACEHOLDER_IMG = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 24 24" fill="none" stroke="%23a1a1aa" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>'

async function buscarProduto() {
    if (!produtoStore.produtos.length) {
        await produtoStore.carregarProdutos()
    }

    // Usa o helper de busca para garantir conversão numérica
    produto.value = produtoStore.buscarPorId(route.params.id as string) || null

    imgAtiva.value = 0
    qty.value = 1
}

watch(() => route.params.id, buscarProduto, { immediate: true })

// Trata URLs relativas do Django Rest Framework (acrescenta a baseURL se necessário)
function formatarUrlImagem(url?: string | null): string {
    if (!url) return PLACEHOLDER_IMG
    if (url.startsWith('http')) return url
    const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/api\/?$/, '')
    return `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`
}

// Lista de imagens tratadas com Fallback
const imagens = computed(() => {
    if (!produto.value) return [PLACEHOLDER_IMG]
    
    const list = [produto.value.imagem_1, produto.value.imagem_2]
        .filter(Boolean)
        .map(img => formatarUrlImagem(img))

    return list.length ? list : [PLACEHOLDER_IMG]
})

const estoqueDisponivel = computed(() => Number(produto.value?.quantidade ?? 0))

const relacionados = computed(() => {
    if (!produto.value) return []
    return produtoStore.produtosDaCategoria(produto.value.categoria_nome || produto.value.categoria)
        .filter(p => p.id !== produto.value?.id)
})

function formatarPreco(valor?: number | string) {
    const num = Number(valor ?? 0)
    return num.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function decrementarQty() {
    if (qty.value > 1) {
        qty.value--
    }
}

function incrementarQty() {
    if (estoqueDisponivel.value > 0 && qty.value < estoqueDisponivel.value) {
        qty.value++
    } else if (estoqueDisponivel.value > 0 && qty.value >= estoqueDisponivel.value) {
        toast.add({
            severity: 'warn',
            summary: 'Estoque Limitado',
            detail: `Apenas ${estoqueDisponivel.value} unidades disponíveis.`,
            life: 2500
        })
    }
}

function aoErroImagem(event: Event) {
    const target = event.target as HTMLImageElement
    target.src = PLACEHOLDER_IMG
}

function adicionarAoCarrinho() {
    if (!produto.value) return

    carrinho.addItem({
        produtoId: produto.value.id,
        nome: produto.value.nome,
        preco: Number(produto.value.preco),
        imagem: imagens.value[0],
        quantidade: qty.value
    })

    toast.add({
        severity: 'success',
        summary: 'Adicionado!',
        detail: `${qty.value}x ${produto.value.nome} no carrinho.`,
        life: 3000
    })

    carrinho.abrir()
}
</script>

<template>
  <div v-if="produto" class="max-w-6xl mx-auto px-4 py-8 animate-fade-in">

    <!-- Breadcrumb Corrigido -->
    <nav class="flex items-center gap-2 text-sm text-zinc-500 mb-6">
      <RouterLink :to="{ name: 'home' }" class="hover:text-orange-500 transition-colors">Início</RouterLink>
      <span>/</span>
      <RouterLink :to="{ name: 'produtos' }" class="hover:text-orange-500 transition-colors">Produtos</RouterLink>
      <span>/</span>
      <span class="text-zinc-900 font-medium truncate max-w-[200px]">{{ produto.nome }}</span>
    </nav>

    <!-- Detalhes do Produto -->
    <div class="grid md:grid-cols-2 gap-8 items-start">
      
      <!-- Galeria de Imagens -->
      <div class="space-y-4">
        <div class="aspect-square rounded-2xl overflow-hidden bg-zinc-100 border border-zinc-200/80 shadow-sm relative group">
          <img 
            :src="imagens[imgAtiva]" 
            :alt="produto.nome" 
            @error="aoErroImagem"
            class="w-full h-full object-cover object-center transition-all duration-300 group-hover:scale-105" 
          />
        </div>

        <!-- Miniaturas se houver mais de uma imagem -->
        <div v-if="imagens.length > 1" class="flex gap-3">
          <button
            v-for="(img, i) in imagens"
            :key="i"
            @click="imgAtiva = i"
            class="w-20 h-20 rounded-xl overflow-hidden border-2 transition-all duration-200 bg-zinc-100 focus:outline-none"
            :class="imgAtiva === i ? 'border-orange-500 ring-2 ring-orange-500/20' : 'border-zinc-200 opacity-70 hover:opacity-100'"
          >
            <img :src="img" @error="aoErroImagem" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>

      <!-- Informações & Compra -->
      <div class="flex flex-col h-full justify-between space-y-6">
        <div>
          <span v-if="produto.categoria_nome" class="text-xs font-semibold uppercase tracking-wider text-orange-600 bg-orange-50 px-3 py-1 rounded-full border border-orange-100">
            {{ produto.categoria_nome }}
          </span>

          <h1 class="text-3xl font-extrabold text-zinc-900 mt-3 tracking-tight">{{ produto.nome }}</h1>
          
          <p class="text-3xl font-black text-orange-500 mt-4">
            {{ formatarPreco(produto.preco) }}
          </p>

          <p class="text-zinc-600 mt-4 leading-relaxed text-sm md:text-base">
            {{ produto.descricao || 'Sem descrição cadastrada para este produto.' }}
          </p>

          <!-- Status do Estoque -->
          <div class="mt-6 flex items-center gap-2">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium"
              :class="estoqueDisponivel > 5 
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                : estoqueDisponivel > 0 
                  ? 'bg-amber-50 text-amber-700 border border-amber-200' 
                  : 'bg-rose-50 text-rose-700 border border-rose-200'"
            >
              <span 
                class="w-2 h-2 rounded-full mr-2"
                :class="estoqueDisponivel > 5 ? 'bg-emerald-500' : estoqueDisponivel > 0 ? 'bg-amber-500' : 'bg-rose-500'"
              />
              {{ estoqueDisponivel > 0 ? `${estoqueDisponivel} unidades em estoque` : 'Produto esgotado' }}
            </span>
          </div>
        </div>

        <!-- Controles de Quantidade e Botão -->
        <div class="pt-6 border-t border-zinc-100 space-y-4">
          <div class="flex items-center gap-4">
            <!-- Selector de Quantidade -->
            <div class="flex items-center border border-zinc-300 rounded-xl overflow-hidden bg-white shadow-sm">
              <button 
                class="px-4 py-3 hover:bg-zinc-100 text-zinc-600 font-bold disabled:opacity-40 disabled:hover:bg-transparent transition-colors" 
                @click="decrementarQty"
                :disabled="qty <= 1 || estoqueDisponivel === 0"
              >
                −
              </button>
              <span class="px-4 font-bold text-zinc-800 min-w-[2.5rem] text-center select-none">{{ qty }}</span>
              <button 
                class="px-4 py-3 hover:bg-zinc-100 text-zinc-600 font-bold disabled:opacity-40 disabled:hover:bg-transparent transition-colors" 
                @click="incrementarQty"
                :disabled="qty >= estoqueDisponivel || estoqueDisponivel === 0"
              >
                +
              </button>
            </div>

            <!-- Botão Adicionar ao Carrinho -->
            <button
              @click="adicionarAoCarrinho"
              :disabled="estoqueDisponivel === 0"
              class="flex-1 bg-orange-500 hover:bg-orange-600 active:scale-[0.99] disabled:bg-zinc-300 disabled:cursor-not-allowed text-white font-bold py-3.5 px-6 rounded-xl shadow-lg shadow-orange-500/20 transition-all duration-200 flex items-center justify-center gap-2"
            >
              <i class="pi pi-shopping-bag text-lg" />
              <span>{{ estoqueDisponivel > 0 ? 'Adicionar ao carrinho' : 'Indisponível' }}</span>
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Seção de Relacionados -->
    <div v-if="relacionados.length" class="mt-16 pt-10 border-t border-zinc-200/60">
      <h2 class="text-xl font-bold text-zinc-900 mb-6 flex items-center gap-2">
        <span>Você também pode gostar</span>
        <span class="h-px flex-1 bg-zinc-200 ml-2"></span>
      </h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-5">
        <ProdutoCard v-for="p in relacionados" :key="p.id" :produto="p" />
      </div>
    </div>

  </div>

  <Loading v-else-if="produtoStore.carregando" />
  <Empty v-else icon="pi pi-box" title="Produto não encontrado" description="O produto procurado não existe ou foi removido do catálogo." />
</template>