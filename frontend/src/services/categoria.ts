import api from '@/api/api'
import type { Categoria } from '@/types/categoria'

export async function todasCategorias(): Promise<Categoria[]>{
    const response = await api.get<Categoria[]>("/categoria/")
    
    return response.data
}