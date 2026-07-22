import { defineStore } from "pinia"
import { ref } from "vue"

import type { Categoria } from "@/types/categoria"

import { todasCategorias } from "@/services/categoria"

export const useCategoriaStore = defineStore("categoria", () => {

    const categorias = ref<Categoria[]>([])

    const loading = ref(false)

    async function carregarCategorias() {

        loading.value = true

        try {

            categorias.value = await todasCategorias()

        } finally {

            loading.value = false

        }

    }

    return {

        categorias,

        loading,

        carregarCategorias

    }

})