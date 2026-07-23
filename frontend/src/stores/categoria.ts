import { defineStore } from "pinia"
import { ref } from "vue"
import type { Categoria } from "@/types/categoria"
import { todasCategorias } from "@/services/categoria"

export const useCategoriaStore = defineStore("categoria", () => {
    const categorias = ref<Categoria[]>([])
    const carregando = ref(false)

    async function carregarCategorias() {
        carregando.value = true
        try {
            categorias.value = await todasCategorias()
        } catch (error) {
            console.error("Erro ao carregar categorias:", error)
        } finally {
            carregando.value = false
        }
    }

    return {
        categorias,
        carregando,
        carregarCategorias
    }
})