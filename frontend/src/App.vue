<script setup lang="ts">
import { onMounted } from 'vue'

import { useLojaStore } from '@/stores/loja'
import { useProdutosStore } from '@/stores/produto'
import { useCategoriaStore } from '@/stores/categoria'

const lojaStore = useLojaStore()
const produtoStore = useProdutosStore()
const categoriaStore = useCategoriaStore()

onMounted(async () => {

    await Promise.all([
        lojaStore.carregarLoja(),
        produtoStore.carregarProdutos(),
        categoriaStore.fetch()
    ])

})
</script>

<template>
    <RouterView />
</template>