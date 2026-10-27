<script setup lang="ts">
import { computed, onMounted } from "vue"
import { storeToRefs } from "pinia"

import HeroBanner from "@/components/layout/HeroBanner.vue"
import Hero from "@/components/layout/Hero.vue"
import Banner from "@/components/layout/Banner.vue"
import CategoriaList from "@/components/catalogo/CategoriaList.vue"
import CategoriaCard from "@/components/catalogo/CategoriaCard.vue"
import ProdutoGrid from "@/components/catalogo/ProdutoGrid.vue"
import Depoiments from "@/components/layout/Depoiments.vue"

import { useProdutosStore } from "@/stores/produto"
import { useCategoriaStore } from "@/stores/categoria"
import { useLojaStore } from "@/stores/loja"

const lojaStore = useLojaStore()
const produtoStore = useProdutosStore()
const categoriaStore = useCategoriaStore()

const { destaques: produtos, carregando: carregandoProdutos } = storeToRefs(produtoStore)
const { categorias } = storeToRefs(categoriaStore)

const categoriasAtivas = computed(() => categorias.value.filter((c) => c.ativo))

onMounted(() => {
    // Cada carga é independente: se uma falhar, as outras continuam
    Promise.allSettled([
        categoriaStore.carregarCategorias(),
        produtoStore.carregarProdutos(),
        lojaStore.carregarLoja(),
    ])
})
</script>

<template>
<div>
    <HeroBanner />
    <Hero />
    <Banner />
    <CategoriaList />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <!-- Categorias: carrossel no celular, grade a partir do sm -->
        <div
            class="-mx-4 px-4 sm:mx-0 sm:px-0 py-3 flex gap-3 overflow-x-auto snap-x snap-mandatory
                   sm:grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 sm:overflow-visible
                   [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        >
            <div
                v-for="categoria in categoriasAtivas"
                :key="categoria.id"
                class="w-[15rem] shrink-0 snap-start sm:w-auto sm:shrink"
            >
                <CategoriaCard :categoria="categoria" />
            </div>
        </div>

        <h2 class="text-xl sm:text-2xl font-bold text-zinc-800 dark:text-white mt-2 sm:mt-4 mb-4 sm:mb-6">
            Destaques
        </h2>

        <ProdutoGrid
            class="mb-8 sm:mb-10"
            :produtos="produtos"
            :carregando="carregandoProdutos"
        />

        <section
            v-for="categoria in categoriasAtivas"
            :key="categoria.id"
            class="mt-10 sm:mt-16"
        >
            <div class="flex justify-between items-center gap-3 mb-4 sm:mb-6">
                <h2 class="text-xl sm:text-2xl font-bold text-zinc-800 dark:text-white truncate">
                    {{ categoria.nome }}
                </h2>

                <RouterLink
                    :to="{ name: 'produtos', query: { categoria: String(categoria.id) } }"
                    class="shrink-0 text-sm font-semibold text-orange-600 dark:text-orange-400 hover:underline"
                >
                    Ver todos
                </RouterLink>
            </div>

            <ProdutoGrid :produtos="produtoStore.produtosDaCategoria(categoria.id)" />
        </section>
    </div>

    <Depoiments />
</div>
</template>