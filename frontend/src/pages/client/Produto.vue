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

async function buscarProduto() {
    if (!produtoStore.produtos.length) {
        await produtoStore.carregarProdutos()
    }

    produto.value = produtoStore.produtos.find(
        p => p.id === Number(route.params.id)
    ) || null

    imgAtiva.value = 0
    qty.value = 1
}

watch(() => route.params.id, buscarProduto, { immediate: true })

const imagens = computed(() =>
    [produto.value?.imagem_1, produto.value?.imagem_2].filter(Boolean)
)

const relacionados = computed(() => {
    if (!produto.value) return []

    return produtoStore.produtos
        .filter(p => p.categoria_nome === produto.value?.categoria_nome && p.id !== produto.value?.id)
        .sort(() => Math.random() - 0.5)
        .slice(0, 4)
})

function formatarPreco(valor: number) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function adicionarAoCarrinho() {
    if (!produto.value) return

    carrinho.addItem({
        produtoId: produto.value.id,
        nome: produto.value.nome,
        preco: produto.value.preco,
        imagem: produto.value.imagem_1,
        quantidade: qty.value
    })

    toast.add({
        severity: 'success',
        summary: 'Carrinho',
        detail: 'Produto adicionado.',
        life: 3000
    })

    carrinho.abrir()
}
</script>

<template>
  <div v-if="produto" class="max-w-6xl mx-auto px-4 py-8">

    <nav class="text-sm text-zinc-500 mb-6">
      <RouterLink :to="{ name: 'home' }" class="hover:text-orange-500">Início</RouterLink>
      /
      <RouterLink :to="{ name: 'categoria', params: { slug: produto.categoria_nome } }" class="hover:text-orange-500">
        {{ produto.categoria_nome }}
      </RouterLink>
      /
      <span class="text-zinc-800 font-medium">{{ produto.nome }}</span>
    </nav>

    <div class="grid md:grid-cols-2 gap-8">
      <div>
        <div class="aspect-square rounded-2xl overflow-hidden bg-zinc-100">
          <img :src="imagens[imgAtiva]" :alt="produto.nome" class="w-full h-full object-cover" />
        </div>

        <div v-if="imagens.length > 1" class="flex gap-2 mt-3">
          <button
            v-for="(img, i) in imagens"
            :key="i"
            @click="imgAtiva = i"
            class="w-16 h-16 rounded-lg overflow-hidden border-2"
            :class="imgAtiva === i ? 'border-orange-500' : 'border-transparent'"
          >
            <img :src="img" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>

      <div>
        <span class="text-xs font-semibold text-orange-600 bg-orange-50 px-3 py-1 rounded-full">
          {{ produto.categoria_nome }}
        </span>

        <h1 class="text-2xl font-bold text-zinc-900 mt-3">{{ produto.nome }}</h1>
        <p class="text-zinc-500 mt-2">{{ produto.descricao }}</p>
        <p class="text-3xl font-bold text-orange-500 mt-4">{{ formatarPreco(produto.preco) }}</p>
        <div class="mb-4 mt-8">
          <span
            class="text-xs font-semibold"
            :class="produto.quantidade> 5 ? 'text-green-600' : produto.quantidade > 0 ? 'text-orange-500' : 'text-red-500'"
          >
            <i class="pi pi-circle-fill text-[8px] mr-1" />
            {{ produto.quantidade > 0 ? `${produto.quantidade} em estoque` : 'Sem estoque' }}
          </span>
        </div>

        <div class="flex items-center gap-3 mt-6">
          <div class="flex items-center border border-zinc-200 rounded-xl overflow-hidden">
            <button class="px-3 py-2 hover:bg-zinc-100" @click="qty > 1 && qty--">−</button>
            <span class="px-4 font-semibold">{{ qty }}</span>
            <button class="px-3 py-2 hover:bg-zinc-100" @click="qty++">+</button>
          </div>

          <button
            @click="adicionarAoCarrinho"
            class="flex-1 bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 rounded-xl transition-colors"
          >
            Adicionar ao carrinho
          </button>
        </div>
      </div>
    </div>

    <div v-if="relacionados.length" class="mt-12">
      <h2 class="text-lg text-center  rounded-2xl font-extrabold text-zinc-900 dark:text-orange-500 ring-2
       ring-orange-500 mb-4">Você também pode gostar!</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-5">
        <ProdutoCard v-for="p in relacionados" :key="p.id" :produto="p" />
      </div>
    </div>

  </div>

  <Loading v-else-if="produtoStore.carregando" />
  <Empty v-else icon="pi pi-box" title="Produto não encontrado" />
</template>