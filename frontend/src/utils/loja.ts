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

  // Hora e dia atuais no fuso de Brasília (independe do aparelho do visitante)
  const partes = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Sao_Paulo',
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).formatToParts(new Date())

  const pegar = (tipo: string) => partes.find((p) => p.type === tipo)?.value ?? ''
  const dia = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(pegar('weekday'))
  const minutos = (Number(pegar('hour')) % 24) * 60 + Number(pegar('minute'))

  const ultimoDia = loja.dias_funcionamento === 'SS' ? 6 : 5
  if (dia === 0 || dia > ultimoDia) return false

  return (
    minutos >= paraMinutos(loja.horario_funcionamento) &&
    minutos < paraMinutos(loja.horario_fechamento)
  )
}