import api from '@/api/api'
import type { Categoria } from '@/types/categoria'

export async function listarCategorias(): Promise<Categoria[]> {
  const response = await api.get('/categoria/')
  return response.data
}
export const todasCategorias = listarCategorias

export async function criarCategoria(
  categoria: FormData | Omit<Categoria, 'id'>
) {
  const isFormData = categoria instanceof FormData
  const response = await api.post('/categoria/', categoria, {
    headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : undefined
  })
  return response.data
}

export async function atualizarCategoria(
  id: number,
  categoria: FormData | Partial<Omit<Categoria, 'id'>>
) {
  const isFormData = categoria instanceof FormData
  const response = await api.patch(
    `/categoria/${id}/`,
    categoria,
    {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : undefined
    }
  )

  return response.data
}

export async function removerCategoria(id: number) {
  await api.delete(`/categoria/${id}/`)
}