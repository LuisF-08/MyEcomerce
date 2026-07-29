<script setup lang="ts">
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import { useDashboardStore } from '@/stores/dashboard'

const props = withDefaults(defineProps<{ verTodosRota?: string }>(), {
  verTodosRota: 'admin-solicitacoes',
})

const dashboard = useDashboardStore()
const router = useRouter()
const { dados } = storeToRefs(dashboard)

const pedidos = computed(() => dados.value?.ultimos_pedidos ?? [])

const expandido = ref<number | null>(null)
function alternar(id: number) {
  expandido.value = expandido.value === id ? null : id
}

function formatarMoeda(valor: number) {
  return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatarCodigo(id: number) {
  return `#${String(id).padStart(4, '0')}`
}

function formatarTelefone(telefone?: string) {
  const d = telefone?.replace(/\D/g, '') ?? ''
  if (d.length === 11) return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`
  if (d.length === 10) return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`
  return telefone ?? ''
}

function tempoRelativo(dataStr: string) {
  const data = new Date(dataStr)
  if (Number.isNaN(data.getTime())) return dataStr

  const diffMin = Math.round((data.getTime() - Date.now()) / 60000)
  const rtf = new Intl.RelativeTimeFormat('pt-BR', { numeric: 'auto' })

  if (Math.abs(diffMin) < 60) return rtf.format(diffMin, 'minute')
  const diffHoras = Math.round(diffMin / 60)
  if (Math.abs(diffHoras) < 24) return rtf.format(diffHoras, 'hour')
  return rtf.format(Math.round(diffHoras / 24), 'day')
}

function iniciais(nome: string) {
  const partes = nome.trim().split(/\s+/)
  return [partes[0]?.[0], partes.at(-1)?.[0]].filter(Boolean).join('').toUpperCase() || '?'
}

const PALETAS = [
  { bg: 'bg-orange-100 dark:bg-orange-500/10', texto: 'text-orange-600 dark:text-orange-400' },
  { bg: 'bg-blue-100 dark:bg-blue-500/10', texto: 'text-blue-600 dark:text-blue-400' },
  { bg: 'bg-emerald-100 dark:bg-emerald-500/10', texto: 'text-emerald-600 dark:text-emerald-400' },
  { bg: 'bg-purple-100 dark:bg-purple-500/10', texto: 'text-purple-600 dark:text-purple-400' },
  { bg: 'bg-pink-100 dark:bg-pink-500/10', texto: 'text-pink-600 dark:text-pink-400' },
]

function avatarDoCliente(nome: string) {
  let hash = 0
  for (const c of nome) hash = (hash * 31 + c.charCodeAt(0)) >>> 0
  return PALETAS[hash % PALETAS.length]
}

interface StatusInfo { label: string; ponto: string; badge: string; valor: string }

const STATUS_MAP: Record<string, StatusInfo> = {
  novo: { label: 'Novo', ponto: 'bg-blue-500', badge: 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400', valor: 'text-zinc-900 dark:text-white' },
  visto: { label: 'Visto', ponto: 'bg-amber-500', badge: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400', valor: 'text-zinc-900 dark:text-white' },
  concluido: { label: 'Concluído', ponto: 'bg-emerald-500', badge: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400', valor: 'text-emerald-600 dark:text-emerald-400' },
  cancelado: { label: 'Cancelado', ponto: 'bg-red-500', badge: 'bg-red-50 text-red-700 dark:bg-red-500/10 dark:text-red-400', valor: 'text-zinc-400 dark:text-zinc-500 line-through' },
}

const STATUS_PADRAO: StatusInfo = {
  label: 'Indefinido',
  ponto: 'bg-zinc-400',
  badge: 'bg-zinc-100 text-zinc-600 dark:bg-zinc-500/10 dark:text-zinc-400',
  valor: 'text-zinc-900 dark:text-white',
}

function statusInfo(status: string): StatusInfo {
  const chave = status?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  return STATUS_MAP[chave] ?? { ...STATUS_PADRAO, label: status || STATUS_PADRAO.label }
}
</script>

<template>
  <div class="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl overflow-hidden">
    <!-- Cabeçalho -->
    <div class="flex items-center justify-between px-4 sm:px-6 py-4">
      <div class="flex items-center gap-3 min-w-0">
        <div class="shrink-0 w-9 h-9 rounded-xl bg-gradient-to-br from-orange-400 to-orange-600 flex items-center justify-center">
          <i class="pi pi-receipt text-white text-sm" />
        </div>
        <h3 class="text-sm font-semibold text-zinc-700 dark:text-zinc-200 truncate">Últimos pedidos</h3>
      </div>

      <span class="shrink-0 text-xs font-semibold px-2.5 py-1 rounded-full bg-orange-50 text-orange-600 dark:bg-orange-500/10 dark:text-orange-400">
        {{ pedidos.length }} {{ pedidos.length === 1 ? 'pedido' : 'pedidos' }}
      </span>
    </div>

    <!-- Vazio -->
    <div v-if="pedidos.length === 0" class="flex flex-col items-center text-center py-12 px-6 text-zinc-400 dark:text-zinc-500">
      <i class="pi pi-inbox text-3xl mb-3 opacity-60" />
      <p class="text-sm">Nenhum pedido chegou por aqui ainda.</p>
    </div>

    <!-- Lista -->
    <div v-else class="divide-y divide-zinc-100 dark:divide-zinc-800">
      <div v-for="(pedido, index) in pedidos" :key="pedido.id">
        <button
          type="button"
          class="w-full flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4 text-left px-4 sm:px-6 py-3
                 hover:bg-zinc-50 dark:hover:bg-zinc-800/60 transition-colors"
          :class="index === 0 && 'bg-orange-50/40 dark:bg-orange-500/[0.04]'"
          @click="alternar(pedido.id)"
        >
          <!-- Avatar + cliente -->
          <div class="flex items-center gap-3 min-w-0">
            <div
              class="shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold"
              :class="[avatarDoCliente(pedido.cliente).bg, avatarDoCliente(pedido.cliente).texto]"
            >
              {{ iniciais(pedido.cliente) }}
            </div>

            <div class="min-w-0">
              <div class="flex items-center gap-2">
                <p class="font-semibold text-zinc-800 dark:text-zinc-100 truncate">{{ pedido.cliente }}</p>
                <span v-if="index === 0" class="shrink-0 text-[10px] font-bold uppercase text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-500/10 px-1.5 py-0.5 rounded-md">
                  Recente
                </span>
              </div>
              <p class="text-xs text-zinc-400 dark:text-zinc-500 font-mono truncate">
                {{ formatarCodigo(pedido.id) }} · {{ tempoRelativo(pedido.criado_em) }}
              </p>
            </div>
          </div>

          <!-- Total + status + seta -->
          <div class="flex items-center justify-between sm:justify-end gap-3 sm:ml-auto pl-[3.25rem] sm:pl-0">
            <div class="text-left sm:text-right">
              <p class="font-bold tabular-nums" :class="statusInfo(pedido.status).valor">
                {{ formatarMoeda(pedido.total) }}
              </p>
              <span class="inline-flex items-center gap-1.5 text-[11px] font-medium px-2 py-0.5 rounded-full mt-1" :class="statusInfo(pedido.status).badge">
                <span class="w-1.5 h-1.5 rounded-full" :class="statusInfo(pedido.status).ponto" />
                {{ statusInfo(pedido.status).label }}
              </span>
            </div>

            <i class="pi pi-chevron-down text-xs text-zinc-300 dark:text-zinc-600 transition-transform" :class="expandido === pedido.id && 'rotate-180'" />
          </div>
        </button>

        <!-- Detalhes: telefone, cidade e itens -->
        <div v-if="expandido === pedido.id" class="bg-zinc-50 dark:bg-zinc-800/40 px-4 sm:px-6 py-3 text-sm text-zinc-600 dark:text-zinc-300 grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
          <a v-if="pedido.telefone" :href="`tel:${pedido.telefone.replace(/\\D/g, '')}`" class="flex items-center gap-2 hover:text-orange-600 dark:hover:text-orange-400" @click.stop>
            <i class="pi pi-phone text-xs text-zinc-400" />
            {{ formatarTelefone(pedido.telefone) }}
          </a>

          <p v-if="pedido.cidade" class="flex items-center gap-2">
            <i class="pi pi-map-marker text-xs text-zinc-400" />
            {{ pedido.cidade }}<template v-if="pedido.estado">, {{ pedido.estado }}</template>
          </p>

          <div v-if="pedido.itens?.length" class="sm:col-span-2 flex flex-wrap gap-1.5 pt-1">
            <span v-for="(item, i) in pedido.itens" :key="i" class="text-xs px-2 py-1 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-700">
              {{ item.quantidade }}x {{ item.produto_nome }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Rodapé -->
    <button
      v-if="pedidos.length > 0"
      type="button"
      class="group w-full flex items-center justify-center gap-1.5 text-xs font-semibold
             text-zinc-500 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-orange-400
             border-t border-zinc-100 dark:border-zinc-800 py-3 transition-colors"
      @click="router.push({ name: props.verTodosRota })"
    >
      Ver todos os pedidos
      <i class="pi pi-arrow-right text-[10px] transition-transform group-hover:translate-x-0.5" />
    </button>
  </div>
</template>