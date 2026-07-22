<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useToast } from "primevue/usetoast"
import { useCarrinhoStore } from "@/stores/carrinho"
import type { Produto } from "@/types/produto"

const props = defineProps<{
    produto: Produto
}>()

const router = useRouter()
const carrinho = useCarrinhoStore()
const toast = useToast()

const imagemErro = ref(false)

function formatarPreco(valor: number) {
    return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })
}

function abrirProduto() {
    router.push({ name: 'produto', params: { id: props.produto.id } })
}

function adicionarAoCarrinho() {
    if (!props.produto) return

    carrinho.addItem({
        produtoId: props.produto.id,
        nome: props.produto.nome,
        preco: props.produto.preco,
        imagem: props.produto.imagem_1,
        quantidade: 1
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
<div
    class="group rounded-3xl overflow-hidden bg-white/90 dark:bg-white/10 backdrop-blur-xl backdrop-saturate-150 border border-zinc-200 dark:border-white/15 shadow-lg shadow-zinc-200/40 dark:shadow-black/40 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 flex flex-col cursor-pointer"
    @click="abrirProduto"
>
    <div class="relative w-full aspect-[4/5] bg-zinc-100 dark:bg-white/5 overflow-hidden">
        <img
            v-if="!imagemErro && produto.imagem_1"
            :src="produto.imagem_1"
            :alt="produto.nome"
            loading="lazy"
            class="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
            @error="imagemErro = true"
        >
        <div
            v-else
            class="w-full h-full flex items-center justify-center bg-zinc-100 dark:bg-white/5 text-zinc-400 dark:text-zinc-500"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3 8.25v7.5A2.25 2.25 0 005.25 18h13.5A2.25 2.25 0 0021 15.75v-7.5A2.25 2.25 0 0018.75 6H5.25A2.25 2.25 0 003 8.25z" />
            </svg>
        </div>

        <div class="absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-white/5"></div>
    </div>

    <div class="p-5 flex flex-col flex-1 backdrop-blur-md">
        <span class="inline-flex w-fit px-3 py-1 rounded-full bg-orange-500/10 dark:bg-orange-400/10 border border-orange-500/20 text-orange-600 dark:text-orange-300 text-xs font-semibold tracking-wide mb-3">
            {{ produto.categoria_nome }}
        </span>

        <h3 class="font-semibold text-zinc-800 leading-snug line-clamp-1">
            {{ produto.nome }}
        </h3>

        <p class="text-zinc-500 dark:text-zinc-400 text-sm mt-1 line-clamp-2 flex-1">
            {{ produto.descricao }}
        </p>

        <div class="flex items-center justify-between mt-4">
            <p class="font-bold text-xl text-orange-500 dark:text-orange-400">
                {{ formatarPreco(produto.preco) }}
            </p>
        
            <div class="flex gap-2">
                <button
                    @click.stop="abrirProduto"
                    class="rounded-xl px-3 py-2 font-semibold border border-zinc-200 text-zinc-600 hover:bg-zinc-100 transition-all"
                >
                    <i class="pi pi-eye"/>
                </button>
        
                <button
                    @click.stop="adicionarAoCarrinho"
                    class="rounded-xl px-5 py-2 font-semibold bg-orange-500 text-white hover:bg-orange-600 transition-all shadow-lg shadow-orange-500/30"
                >
                    <i class="pi pi-cart-plus"/>
                </button>
            </div>
        </div>
    </div>
</div>
</template>