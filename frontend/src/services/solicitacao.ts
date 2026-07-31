import api from '@/api/api'

import type {
  Solicitacao
} from '@/types/solicitacao'


export async function listarSolicitacoes(): Promise<Solicitacao[]> {

  const response = await api.get<Solicitacao[]>(
    '/solicitacao/'
  )

  return response.data
}


export async function buscarSolicitacao(
  id: number
): Promise<Solicitacao> {

  const response = await api.get<Solicitacao>(
    `/solicitacao/${id}/`
  )

  return response.data
}


export async function atualizarStatusSolicitacao(
  id: number,
  status: string
): Promise<Solicitacao> {

  const response = await api.patch<Solicitacao>(
    `/solicitacao/${id}/status/`,
    {
      status
    }
  )

  return response.data
}


export async function removerSolicitacao(
  id: number
): Promise<void> {

  await api.delete(
    `/solicitacao/${id}/`
  )
}
