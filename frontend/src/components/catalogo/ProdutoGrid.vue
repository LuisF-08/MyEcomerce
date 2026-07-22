<script setup lang="ts">
import type { Produto } from "@/types/produto"
import ProdutoCard from "@/components/catalogo/ProdutoCard.vue"

const props = withDefaults(defineProps<{
    produtos: Produto[]
    carregando?: boolean
}>(), {
    carregando: false
})
</script>

<template>
<div>
    <div
        v-if="carregando"
        class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-6"
    >
        <div
            v-for="n in 10"
            :key="n"
            class="bg-white rounded-2xl ring-1 ring-zinc-100 overflow-hidden animate-pulse"
        >
            <div class="w-full aspect-[4/5] bg-zinc-200"></div>
            <div class="p-4 space-y-3">
                <div class="h-4 bg-zinc-200 rounded w-3/4"></div>
                <div class="h-3 bg-zinc-200 rounded w-full"></div>
                <div class="h-3 bg-zinc-200 rounded w-2/3"></div>
                <div class="h-6 bg-zinc-200 rounded w-1/2 mt-4"></div>
            </div>
        </div>
    </div>

    <!-- Estado vazio -->
    <div
        v-else-if="!produtos.length"
        class="flex flex-col items-center justify-center py-20 text-center"
    >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-14 h-14 text-zinc-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
        </svg>
        <p class="text-zinc-500 font-medium">Nenhum produto encontrado</p>
        <p class="text-zinc-400 text-sm mt-1">Tente ajustar os filtros ou volte mais tarde</p>
    </div>

    <!-- Grid de produtos -->
    <div
        v-else
        class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-6"
    >
        <ProdutoCard
            v-for="produto in produtos"
            :key="produto.id"
            :produto="produto"
        />
    </div>

</div>
</template>