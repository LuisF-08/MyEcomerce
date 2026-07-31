import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Loja } from '@/types/loja'
import { obterLoja } from '@/services/loja'

export const useLojaStore = defineStore('loja', () => {

    const loja = ref<Loja | null>(null)
    const carregando = ref(false)
    const erro = ref<string | null>(null)

    async function carregarLoja() {

        // Se já carregou, não busca novamente
        if (loja.value) {
            return
        }

        carregando.value = true
        erro.value = null

        try {

            loja.value = await obterLoja()

        } catch (error) {

            console.error('Erro ao carregar loja:', error)

            erro.value = 'Não foi possível carregar os dados da loja.'

        } finally {

            carregando.value = false

        }
    }

    return {
        loja,
        carregando,
        erro,
        carregarLoja
    }
})
