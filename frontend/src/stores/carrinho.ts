import { defineStore } from "pinia"
import { ref, computed } from "vue"

import type { ItemCarrinho } from "@/types/carrinho"

export const useCarrinhoStore = defineStore("carrinho", () => {

    const itens = ref<ItemCarrinho[]>(carregarCarrinho())

    const aberto = ref(false)

    const quantidadeItens = computed(() => {
        return itens.value.reduce(
            (total, item) => total + item.quantidade,
            0
        )
    })

    const valorTotal = computed(() => {
        return itens.value.reduce(
            (total, item) =>
                total + item.preco * item.quantidade,
            0
        )
    })

    function carregarCarrinho(): ItemCarrinho[] {
        try {
            const dados = localStorage.getItem("carrinho")
            if (!dados) {
                return []
            }
            return JSON.parse(dados)
        }
        catch {
            return []
        }
    }

    function salvarCarrinho() {
        localStorage.setItem(
            "carrinho",
            JSON.stringify(itens.value)
        )
    }

    function abrir() {
        aberto.value = true
    }

    function fechar() {
        aberto.value = false
    }

    function toggle() {
        aberto.value = !aberto.value
    }

    function addItem(item: ItemCarrinho) {

        const existente = itens.value.find( p => p.produtoId === item.produtoId )

        if (existente) {
            existente.quantidade++
        }
        else {
            itens.value.push({...item, quantidade: 1 })
        }
        salvarCarrinho()
    }

    function removerItem(produtoId: number){
        itens.value = itens.value.filter(
            item => item.produtoId !== produtoId
        )
        salvarCarrinho()
    }

    function incrementar(produtoId: number){
        const item = itens.value.find(
            item => item.produtoId === produtoId
        )
        if(!item) return
        item.quantidade++
        salvarCarrinho()
    }

    function diminuir(produtoId: number){
        const item = itens.value.find(
            item => item.produtoId === produtoId
        )
        if(!item) return

        if(item.quantidade > 1){
            item.quantidade--
        } else {
            removerItem(produtoId)
        }
        salvarCarrinho()
    }

    function limpar(){
        itens.value = []
        salvarCarrinho()
    }

    function existe(produtoId: number) {
        return itens.value.some(
            item => item.produtoId === produtoId
        )
    }

    function quantidade(produtoId: number){
        const item = itens.value.find(
            i => i.produtoId === produtoId
        )
        return item?.quantidade || 0
    }

    return {

        itens,
        aberto,

        quantidadeItens,
        valorTotal,

        abrir,
        fechar,
        toggle,

        addItem,
        removerItem,
        incrementar,
        diminuir,
        limpar,

        existe,
        quantidade

    }

})