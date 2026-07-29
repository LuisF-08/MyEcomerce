import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Produto } from '@/types/produto'

import {
    listarProdutos,
    criarProduto,
    atualizarProduto,
    removerProduto
} from '@/services/produto'

export const useProdutosStore = defineStore('produtos', () => {

    const produtos = ref<Produto[]>([])
    const destaques = ref<Produto[]>([])
    const carregando = ref(false)
    const erro = ref<string | null>(null)

    async function carregarProdutos() {
    carregando.value = true
    erro.value = null

    try {
      produtos.value = await listarProdutos()

      destaques.value = produtos.value.filter(
        produto => produto.destaque
      )

    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
        erro.value = 'Não foi possível carregar os produtos.'
    } finally {
        carregando.value = false
    }
    }

    async function criar(
    produto: Omit<Produto, 'id' | 'categoria_nome'>
    ) {
    const novoProduto = await criarProduto(produto)

    produtos.value.push(novoProduto)

    if (novoProduto.destaque) {
        destaques.value.push(novoProduto)
    }

    return novoProduto
    }

    async function atualizar(
    id: number,
    dados: Partial<Omit<Produto, 'id' | 'categoria_nome'>>
    ) {
    const produtoAtualizado = await atualizarProduto(id, dados)

    const index = produtos.value.findIndex(
        produto => produto.id === id
    )

    if (index !== -1) {
        produtos.value[index] = produtoAtualizado
    }

    destaques.value = produtos.value.filter(
        produto => produto.destaque
    )

    return produtoAtualizado
    }

    async function remover(id: number) {
    await removerProduto(id)

    produtos.value = produtos.value.filter(
        produto => produto.id !== id
    )

    destaques.value = destaques.value.filter(
        produto => produto.id !== id
    )
    }

    function buscarPorId(id: number | string) {
    return produtos.value.find(
        produto => Number(produto.id) === Number(id)
    )
    }

    function produtosDaCategoria(
    categoriaIdentificador: number | string
    ) {
    return produtos.value
     .filter(produto => {
        if (typeof categoriaIdentificador === 'number') {
            return produto.categoria === categoriaIdentificador
        }

        return produto.categoria_nome === categoriaIdentificador
        })
        .slice(0, 4)
    }

    return {
    produtos,
    destaques,
    carregando,
    erro,

    carregarProdutos,
    criar,
    atualizar,
    remover,

    buscarPorId,
    produtosDaCategoria
    }
})