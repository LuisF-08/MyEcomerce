import api from '@/api/api'
import type { Produto } from '@/types/produto'

export async function listarProdutos(): Promise<Produto[]> {
  const response = await api.get('/produto/')
  return response.data.results ?? response.data
}

export async function criarProduto(produtoData: FormData | 
        Omit<Produto, 'id' | 'categoria_nome'>) {
  const response = await api.post('/produto/', produtoData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export async function atualizarProduto(
  id: number,
  produtoData: FormData | Partial<Omit<Produto, 'id' | 'categoria_nome'>>
) {
  const response = await api.patch(`/produto/${id}/`, produtoData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export async function removerProduto(id: number) {
  await api.delete(`/produto/${id}/`)
}