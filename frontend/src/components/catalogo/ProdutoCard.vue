<script setup lang="ts">
import { useRouter } from "vue-router"
import { useToast } from "primevue/usetoast"
import { useCarrinhoStore } from "@/stores/carrinho"
import type { Produto } from "@/types/produto"
import ImagemComFallback from "@/components/ui/ImagemComFallback.vue"

const props = defineProps<{
    produto: Produto
}>()

const router = useRouter()
const carrinho = useCarrinhoStore()
const toast = useToast()

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
    class="group rounded-2xl sm:rounded-3xl overflow-hidden bg-white/90 dark:bg-white/10 backdrop-blur-xl backdrop-saturate-150 border border-zinc-200 dark:border-white/15 shadow-lg shadow-zinc-200/40 dark:shadow-black/40 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 flex flex-col cursor-pointer"
    @click="abrirProduto"
>
    <div class="relative overflow-hidden">
        <ImagemComFallback
            :src="produto.imagem_1"
            :alt="produto.nome"
            aspect="aspect-[4/5]"
            class="group-hover:scale-105 transition-transform duration-500"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-white/5"></div>
    </div>

    <div class="p-3 sm:p-5 flex flex-col flex-1 backdrop-blur-md">
        <span class="inline-flex w-fit px-2 sm:px-3 py-0.5 sm:py-1 rounded-full bg-orange-500/10 dark:bg-orange-400/10 border border-orange-500/20 text-orange-600 dark:text-orange-300 text-[10px] sm:text-xs font-semibold tracking-wide mb-2 sm:mb-3">
            {{ produto.categoria_nome }}
        </span>

        <h3 class="font-semibold text-sm sm:text-base text-zinc-800 leading-snug line-clamp-1">
            {{ produto.nome }}
        </h3>

        <p class="text-zinc-500 dark:text-zinc-400 text-xs sm:text-sm mt-1 line-clamp-2 flex-1">
            {{ produto.descricao }}
        </p>

        <div class="flex items-center justify-between gap-2 mt-3 sm:mt-4">
            <p class="font-bold text-base sm:text-xl text-orange-500 dark:text-orange-400 truncate">
                {{ formatarPreco(produto.preco) }}
            </p>

            <div class="flex gap-1.5 sm:gap-2 shrink-0">
                <button
                    @click.stop="abrirProduto"
                    class="rounded-lg sm:rounded-xl px-2.5 sm:px-3 py-1.5 sm:py-2 font-semibold border border-zinc-200 text-zinc-600 hover:bg-zinc-100 transition-all"
                >
                    <i class="pi pi-eye text-sm"/>
                </button>

                <button
                    @click.stop="adicionarAoCarrinho"
                    class="rounded-lg sm:rounded-xl px-3 sm:px-5 py-1.5 sm:py-2 font-semibold bg-orange-500 text-white hover:bg-orange-600 transition-all shadow-lg shadow-orange-500/30"
                >
                    <i class="pi pi-cart-plus text-sm"/>
                </button>
            </div>
        </div>
    </div>
</div>
</template>