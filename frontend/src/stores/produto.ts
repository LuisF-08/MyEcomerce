import { defineStore } from "pinia";
import { ref } from "vue";
import type { Produto } from "@/types/produto";
import { listarProdutos } from "@/services/produto";
export const useProdutosStore = defineStore("produtos", () => {
    const produtos = ref<Produto[]>([])
    const destaques = ref<Produto[]>([])

    const carregando = ref(false)
    
    async function carregarProdutos() {
        carregando.value = true
        try {
            produtos.value = await listarProdutos()
        } finally {
            carregando.value = false
        }
    }

    async function carregarDestaques() {
        await carregarProdutos()

        destaques.value = produtos.value.filter(
            p => p.destaque
        )
    }

    function produtosDaCategoria(id: number) {
        return produtos.value
            .filter(p => p.categoria === id)
            .slice(0,4)
    }

    

    return {
        produtos,
        destaques,
        carregando,
        carregarProdutos,
        carregarDestaques,
        produtosDaCategoria
    }

})