<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProdutosStore } from '@/stores/produto'
import { useCategoriaStore } from '@/stores/categoria'
import ProdutoCard from '@/components/catalogo/ProdutoCard.vue'
import Empty from '@/components/common/Empty.vue'
import Loading from '@/components/common/Loading.vue'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'

const produtoStore = useProdutosStore()
const categoriaStore = useCategoriaStore()
const route = useRoute()

const busca = ref((route.query.q as string) || '')
const categoriaSelecionada = ref( 'Todos' || (route.params.slug as string))
const ordenacao = ref('relevancia')

const opcoesOrdenacao = [
    { label: 'Relevância', value: 'relevancia' },
    { label: 'Menor preço', value: 'preco_asc' },
    { label: 'Maior preço', value: 'preco_desc' },
    { label: 'Nome A-Z', value: 'nome' }
]

onMounted(async () => {
    if (!produtoStore.produtos.length) await produtoStore.carregarProdutos()
    if (!categoriaStore.categorias.length) await categoriaStore.fetch()
})

watch(() => route.query.q, valor => busca.value = (valor as string) || '')
watch(() => route.params.slug, valor => categoriaSelecionada.value = (valor as string) || 'Todos')

const produtosFiltrados = computed(() => {
    let lista = [...produtoStore.produtos]

    if (categoriaSelecionada.value !== 'Todos') {
        lista = lista.filter(p => p.categoria_nome === categoriaSelecionada.value)
    }

    if (busca.value.trim()) {
        const texto = busca.value.toLowerCase()
        lista = lista.filter(p =>
            p.nome.toLowerCase().includes(texto) ||
            p.descricao.toLowerCase().includes(texto)
        )
    }

    switch (ordenacao.value) {
        case 'preco_asc': lista.sort((a, b) => a.preco - b.preco); break
        case 'preco_desc': lista.sort((a, b) => b.preco - a.preco); break
        case 'nome': lista.sort((a, b) => a.nome.localeCompare(b.nome)); break
    }

    return lista
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8">

    <div class="flex flex-col md:flex-row gap-4 mb-6">
      <InputText v-model="busca" placeholder="Buscar produto..." class="w-full md:flex-1" />

      <Select
        v-model="categoriaSelecionada"
        :options="['Todos', ...categoriaStore.categorias.map(c => c.nome)]"
        class="w-full md:w-56"
      />

      <Select
        v-model="ordenacao"
        :options="opcoesOrdenacao"
        optionLabel="label"
        optionValue="value"
        class="w-full md:w-56"
      />
    </div>

    <p class="text-sm text-zinc-500 mb-4">
      {{ produtosFiltrados.length }} produtos encontrados
    </p>

    <Loading v-if="produtoStore.carregando" />

    <Empty
      v-else-if="!produtosFiltrados.length"
      icon="pi pi-search"
      title="Nenhum produto encontrado"
      description="Tente buscar por outro termo ou categoria."
    />

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
      <ProdutoCard
        v-for="produto in produtosFiltrados"
        :key="produto.id"
        :produto="produto"
      />
    </div>

  </div>
</template>