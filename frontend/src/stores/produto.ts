import { defineStore } from "pinia"
import { ref } from "vue"
import type { Produto } from "@/types/produto"
import { listarProdutos } from "@/services/produto"

export const useProdutosStore = defineStore("produtos", () => {
    const produtos = ref<Produto[]>([])
    const destaques = ref<Produto[]>([])
    const carregando = ref(false)

    async function carregarProdutos() {
        carregando.value = true
        try {
            produtos.value = await listarProdutos()
        } catch (error) {
            console.error("Erro ao carregar produtos:", error)
        } finally {
            carregando.value = false
        }
    }

    async function carregarDestaques() {
        if (!produtos.value.length) {
            await carregarProdutos()
        }
        destaques.value = produtos.value.filter(p => p.destaque)
    }

    // Busca aceitando string ou number (evita erros ao passar route.params.id)
    function buscarPorId(id: number | string): Produto | undefined {
        return produtos.value.find(p => Number(p.id) === Number(id))
    }

    // Filtra por Categoria aceitando ID ou Nome
    function produtosDaCategoria(categoriaIdentificador: number | string) {
        return produtos.value
            .filter(p => {
                if (typeof categoriaIdentificador === 'number') {
                    return p.categoria === categoriaIdentificador
                }
                return p.categoria_nome === categoriaIdentificador
            })
            .slice(0, 4)
    }

    return {
        produtos,
        destaques,
        carregando,
        carregarProdutos,
        carregarDestaques,
        buscarPorId,
        produtosDaCategoria
    }
})