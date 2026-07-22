import api from "@/api/api"
import type { Produto } from "@/types/produto"

export async function listarProdutos(): Promise<Produto[]> {

    const response = await api.get<Produto[]>("/produto/")

    return response.data
}