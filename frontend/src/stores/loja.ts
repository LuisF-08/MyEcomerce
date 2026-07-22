import { defineStore } from "pinia"
import { ref } from "vue"

import type { Loja } from "@/types/loja"

import { obterLoja } from "@/services/loja"

export const useLojaStore = defineStore("loja", () => {

    const loja = ref<Loja | null>(null)

    const carregando = ref(false)

    async function carregarLoja() {

        carregando.value = true

        try {

            loja.value = await obterLoja()

        }

        finally {

            carregando.value = false

        }

    }

    return {

        loja,
        carregando,
        carregarLoja

    }

})