import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Categoria } from '@/types/categoria'

import {
  listarCategorias,
  criarCategoria,
  atualizarCategoria,
  removerCategoria
} from '@/services/categoria'


export const useCategoriaStore = defineStore(
  'categorias',
  () => {

    const categorias = ref<Categoria[]>([])

    const carregando = ref(false)

    const erro = ref<string | null>(null)


    async function carregarCategorias() {

      carregando.value = true
      erro.value = null

      try {

        categorias.value =
          await listarCategorias()

      } catch (error) {

        console.error(
          'Erro ao carregar categorias:',
          error
        )

        erro.value =
          'Não foi possível carregar as categorias.'

      } finally {

        carregando.value = false

      }
    }


    async function criar(
      dados: FormData | Omit<Categoria, 'id'>
    ) {

      const novaCategoria =
        await criarCategoria(dados)

      categorias.value.push(
        novaCategoria
      )

      return novaCategoria
    }


    async function atualizar(
      id: number,
      dados: FormData | Partial<Omit<Categoria, 'id'>>
    ) {

      const categoriaAtualizada =
        await atualizarCategoria(
          id,
          dados
        )

      const index =
        categorias.value.findIndex(
          categoria =>
            categoria.id === id
        )

      if (index !== -1) {

        categorias.value[index] =
          categoriaAtualizada

      }

      return categoriaAtualizada
    }


    async function remover(
      id: number
    ) {

      await removerCategoria(id)

      categorias.value =
        categorias.value.filter(
          categoria =>
            categoria.id !== id
        )
    }


    function buscarPorId(
      id: number | string
    ) {

      return categorias.value.find(
        categoria =>
          Number(categoria.id) ===
          Number(id)
      )
    }


    return {

      categorias,
      carregando,
      erro,

      carregarCategorias,
      criar,
      atualizar,
      remover,
      buscarPorId

    }
  }
)
