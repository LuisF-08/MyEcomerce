import api from '@/api/api'
import type { Solicitcao } from '@/types/solicitacao'

export async function listaSolicitacoes(): Promise<Solicitcao[]> {
    const response = await api.get<Solicitcao[]>("/solicitacoes/")

    return response.data
}