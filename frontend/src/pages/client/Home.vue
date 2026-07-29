<script setup lang="ts">
import { ref, onMounted } from "vue"

// Layout & Componentes
import Navbar from "@/components/layout/Navbar.vue"
import Hero from "@/components/layout/Hero.vue"
import Banner from "@/components/layout/Banner.vue"
import CategoriaList from "@/components/catalogo/CategoriaList.vue"
import CategoriaCard from "@/components/catalogo/CategoriaCard.vue"
import ProdutoGrid from "@/components/catalogo/ProdutoGrid.vue"

// Serviços e Stores
import { todasCategorias } from "@/services/categoria"
import { useProdutosStore } from "@/stores/produto"
import { storeToRefs } from "pinia"
import { useLojaStore } from "@/stores/loja"
import Toast from 'primevue/toast';
const lojaStore = useLojaStore()

// Tipos
import type { Categoria } from "@/types/categoria"
import Footer from "@/components/layout/Footer.vue"
import Depoiments from "@/components/layout/Depoiments.vue"

// Estados e Stores
const categorias = ref<Categoria[]>([])
const produtoStore = useProdutosStore()
const { destaques: produtos, carregando: carregandoProdutos } = storeToRefs(produtoStore)

onMounted(async () => {
    categorias.value = await todasCategorias()
    await produtoStore.carregarDestaques()
    await lojaStore.carregarLoja()
})
</script>

<template>
<div>
    <Hero />
    <Banner />
    <CategoriaList />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <!-- Chips de categoria: rolagem horizontal no mobile, quebra em linhas a partir do sm -->
        <div
            class="flex sm:flex-wrap gap-3 py-4 sm:py-6 overflow-x-auto sm:overflow-visible
                   -mx-4 px-4 sm:mx-0 sm:px-0 snap-x snap-mandatory
                   [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
        >
            <div
                v-for="categoria in categorias"
                :key="categoria.id"
                class="shrink-0 snap-start"
            >
                <CategoriaCard :categoria="categoria" />
            </div>
        </div>

        <h2 class="text-xl sm:text-2xl font-bold text-zinc-800 mt-2 sm:mt-4 mb-4 sm:mb-6">
            Destaques
        </h2>

        <ProdutoGrid class="mb-8 sm:mb-10"
            :produtos="produtos"
            :carregando="carregandoProdutos"
        />

        <section
            v-for="categoria in categorias"
            :key="categoria.id"
            class="mt-10 sm:mt-16"
        >

            <div class="flex justify-between items-center gap-3 mb-4 sm:mb-6">

                <h2 class="text-xl sm:text-2xl font-bold truncate">
                    {{ categoria.nome }}
                </h2>

                <RouterLink
                    :to="`/categoria/${categoria.id}`"
                    class="shrink-0 text-sm font-semibold text-orange-600 dark:text-orange-400 hover:underline"
                >
                    Ver todos
                </RouterLink>

            </div>

            <ProdutoGrid
                :produtos="produtoStore.produtosDaCategoria(categoria.id)"
            />
        </section>
    </div>
    <Depoiments />
</div>
</template>