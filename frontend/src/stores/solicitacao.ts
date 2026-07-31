import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Solicitacao } from '@/types/solicitacao'

import {
  listarSolicitacoes,
  atualizarStatusSolicitacao,
  removerSolicitacao
} from '@/services/solicitacao'


export const useSolicitacaoStore = defineStore(
  'solicitacoes',
  () => {

    const solicitacoes = ref<Solicitacao[]>([])

    const solicitacaoSelecionada =
      ref<Solicitacao | null>(null)

    const carregando = ref(false)

    const erro = ref<string | null>(null)


    async function carregarSolicitacoes() {

      carregando.value = true
      erro.value = null

      try {

        solicitacoes.value =
          await listarSolicitacoes()

      } catch (error: any) {

        console.error(
          'Erro ao carregar solicitações:',
          error?.response?.data ?? error
        )

        erro.value =
          'Não foi possível carregar as solicitações.'

      } finally {

        carregando.value = false

      }
    }


    async function atualizarStatus(
      id: number,
      status: string
    ) {

      try {

        const atualizada =
          await atualizarStatusSolicitacao(
            id,
            status
          )


        const index =
          solicitacoes.value.findIndex(
            s => s.id === id
          )


        if (index !== -1) {

          solicitacoes.value[index] =
            atualizada

        }


        if (
          solicitacaoSelecionada.value?.id === id
        ) {

          solicitacaoSelecionada.value =
            atualizada

        }


        return atualizada

      } catch (error: any) {

        console.error(
          'Erro ao atualizar status:',
          error?.response?.data ?? error
        )

        throw error
      }
    }


    async function remover(id: number) {

      await removerSolicitacao(id)

      solicitacoes.value =
        solicitacoes.value.filter(
          s => s.id !== id
        )


      if (
        solicitacaoSelecionada.value?.id === id
      ) {

        solicitacaoSelecionada.value = null

      }
    }


    function buscarPorId(
      id: number | string
    ) {

      return solicitacoes.value.find(
        s =>
          Number(s.id) === Number(id)
      )

    }


    return {

      solicitacoes,
      solicitacaoSelecionada,
      carregando,
      erro,

      carregarSolicitacoes,
      atualizarStatus,
      remover,
      buscarPorId

    }

  }
)