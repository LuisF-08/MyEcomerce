import api from "@/api/api"
import type { Loja } from "@/types/loja"

export async function obterLoja(): Promise<Loja> {
    const response = await api.get<Loja>("/loja/1/")
    return response.data
}