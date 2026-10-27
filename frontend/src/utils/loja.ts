import type { Loja } from '@/types/loja'

export function formatarHora(h?: string | null): string {
  return h ? h.slice(0, 5) : ''
}

export function diasLabel(d?: string | null): string {
  return d === 'SS' ? 'Seg–Sáb' : 'Seg–Sex'
}

export function whatsappLink(loja: Loja | null | undefined, mensagem = ''): string {
  const numero = (loja?.whatsapp ?? '').replace(/\D/g, '')
  if (!numero) return '#'
  const completo = numero.startsWith('55') ? numero : `55${numero}`
  return `https://wa.me/${completo}${mensagem ? `?text=${encodeURIComponent(mensagem)}` : ''}`
}

function paraMinutos(h: string): number {
  const [hh = '0', mm = '0'] = h.split(':')
  return Number(hh) * 60 + Number(mm)
}

export function lojaAberta(loja: Loja | null | undefined): boolean {
  if (!loja?.horario_funcionamento || !loja.horario_fechamento) return false
  const agora = new Date()
  const dia = agora.getDay()
  const ultimoDia = loja.dias_funcionamento === 'SS' ? 6 : 5
  if (dia === 0 || dia > ultimoDia) return false
  const minutos = agora.getHours() * 60 + agora.getMinutes()
  return (
    minutos >= paraMinutos(loja.horario_funcionamento) &&
    minutos < paraMinutos(loja.horario_fechamento)
  )
}