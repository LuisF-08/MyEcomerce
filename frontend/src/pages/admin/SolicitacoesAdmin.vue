<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import { useSolicitacaoStore } from '@/stores/solicitacao'
import { useToast } from 'primevue/usetoast'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import Button from 'primevue/button'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import Avatar from 'primevue/avatar'
import Divider from 'primevue/divider'

const toast = useToast()
const store = useSolicitacaoStore()
const { solicitacoes, solicitacaoSelecionada } = storeToRefs(store)

/* ------------------------------------------------------------------ */
/* Status: a API usa CÓDIGOS (AGP, NOV, VIS, CON, CAN).                */
/* O texto em português é só para exibição.                            */
/* ------------------------------------------------------------------ */
type StatusCodigo = 'AGP' | 'NOV' | 'VIS' | 'CON' | 'CAN'

interface StatusInfo {
  label: string
  severity: 'info' | 'warn' | 'success' | 'danger' | 'secondary'
  icon: string
  color: string
}

const STATUS: Record<StatusCodigo, StatusInfo> = {
  AGP: { label: 'Aguardando pagamento', severity: 'secondary', icon: 'pi pi-wallet', color: 'text-zinc-500' },
  NOV: { label: 'Novo', severity: 'info', icon: 'pi pi-sparkles', color: 'text-blue-500' },
  VIS: { label: 'Visto', severity: 'warn', icon: 'pi pi-eye', color: 'text-amber-500' },
  CON: { label: 'Concluído', severity: 'success', icon: 'pi pi-check-circle', color: 'text-emerald-500' },
  CAN: { label: 'Cancelado', severity: 'danger', icon: 'pi pi-times-circle', color: 'text-red-500' },
}

const INFO_PADRAO: StatusInfo = {
  label: 'Desconhecido',
  severity: 'secondary',
  icon: 'pi pi-question-circle',
  color: 'text-zinc-400',
}

function infoStatus(codigo: string): StatusInfo {
  return STATUS[codigo as StatusCodigo] ?? { ...INFO_PADRAO, label: codigo || INFO_PADRAO.label }
}

interface FiltroOption {
  label: string
  value: 'TODOS' | StatusCodigo
  icon: string
  color: string
}

const filtroOptions: FiltroOption[] = [
  { label: 'Todos', value: 'TODOS', icon: 'pi pi-list', color: 'text-zinc-600' },
  ...(Object.keys(STATUS) as StatusCodigo[]).map((codigo) => ({
    label: STATUS[codigo].label,
    value: codigo,
    icon: STATUS[codigo].icon,
    color: STATUS[codigo].color,
  })),
]

// Opções do Select de troca de status (não inclui "Aguardando pagamento",
// que só muda automaticamente quando o pagamento é aprovado)
const statusOptions = (['NOV', 'VIS', 'CON', 'CAN'] as StatusCodigo[]).map((codigo) => ({
  label: STATUS[codigo].label,
  value: codigo,
}))

const filtro = ref<FiltroOption>(filtroOptions[0]!)

onMounted(async () => {
  await store.carregarSolicitacoes()
})

const filtradas = computed(() => {
  if (filtro.value.value === 'TODOS') return solicitacoes.value
  return solicitacoes.value.filter((s) => s.status === filtro.value.value)
})

function quantidadePorStatus(valor: string) {
  if (valor === 'TODOS') return solicitacoes.value.length
  return solicitacoes.value.filter((s) => s.status === valor).length
}

/* ------------------------------------------------------------------ */
/* Formatação                                                          */
/* ------------------------------------------------------------------ */
function preco(valor: number | string | undefined | null) {
  const numero = Number(valor)
  if (Number.isNaN(numero)) return 'R$ 0,00'
  return `R$ ${numero.toFixed(2).replace('.', ',')}`
}

function formatDate(data: string | undefined) {
  if (!data) return '-'
  const date = new Date(data)
  if (Number.isNaN(date.getTime())) return '-'
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function endereco(solicitacao: (typeof solicitacoes.value)[number]) {
  if (!solicitacao.rua) return ''
  const partes = [
    solicitacao.rua,
    solicitacao.numero,
    solicitacao.bairro,
    solicitacao.cidade,
    solicitacao.estado,
  ].filter(Boolean)
  return partes.join(', ')
}

function iniciais(nome: string) {
  if (!nome) return '?'
  const partes = nome.trim().split(/\s+/)
  const primeira = partes[0]?.[0] || ''
  const ultima = partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : ''
  return (primeira + ultima).toUpperCase()
}

/* ------------------------------------------------------------------ */
/* Ações                                                               */
/* ------------------------------------------------------------------ */
async function changeStatus(id: number, status: string) {
  try {
    await store.atualizarStatus(id, status)
    toast.add({
      severity: 'success',
      summary: 'Sucesso',
      detail: 'Status atualizado!',
      life: 3000,
    })
  } catch (error) {
    console.error('Erro ao atualizar status:', error)
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: 'Não foi possível atualizar o status.',
      life: 3000,
    })
  }
}

function abrirWhatsApp(telefone: string) {
  const numero = telefone.replace(/\D/g, '')
  if (!numero) {
    toast.add({
      severity: 'warn',
      summary: 'Telefone inválido',
      detail: 'A solicitação não possui um telefone válido.',
      life: 3000,
    })
    return
  }
  window.open(`https://wa.me/55${numero}`, '_blank')
}

function selecionar(solicitacao: (typeof solicitacoes.value)[number]) {
  solicitacaoSelecionada.value = solicitacao
}
</script>

<template>
  <div class="space-y-5">

    <!-- Cabeçalho -->
    <div class="flex items-center gap-3">
      <div class="w-11 h-11 rounded-xl bg-orange-100 flex items-center justify-center">
        <i class="pi pi-shopping-bag text-orange-500 text-lg" />
      </div>
      <div>
        <h2 class="text-lg font-bold text-zinc-900">Solicitações</h2>
        <p class="text-sm text-zinc-500">Pedidos recebidos pelo WhatsApp e pelo Mercado Pago</p>
      </div>
    </div>

    <!-- Filtros -->
    <SelectButton
      v-model="filtro"
      :options="filtroOptions"
      optionLabel="label"
      dataKey="value"
      class="flex-wrap"
    >
      <template #option="{ option }">
        <div class="flex items-center gap-2 px-1">
          <i :class="[option.icon, option.color]" />
          <span class="font-medium">{{ option.label }}</span>
          <span
            class="text-xs rounded-full px-1.5 py-0.5 min-w-[1.25rem] text-center"
            :class="filtro.value === option.value ? 'bg-white/20 text-white' : 'bg-zinc-100 text-zinc-500'"
          >
            {{ quantidadePorStatus(option.value) }}
          </span>
        </div>
      </template>
    </SelectButton>

    <!-- Erro -->
    <div
      v-if="store.erro"
      class="flex items-center gap-2 text-sm text-red-600 bg-red-50 border border-red-100 rounded-xl p-3"
    >
      <i class="pi pi-exclamation-triangle" />
      {{ store.erro }}
    </div>

    <div class="flex flex-col lg:flex-row gap-4 items-stretch lg:items-start">

      <!-- Tabela -->
      <div class="flex-1 min-w-0 w-full bg-white border border-zinc-200 rounded-2xl overflow-x-auto shadow-sm">
        <DataTable
          :value="filtradas"
          v-model:selection="solicitacaoSelecionada"
          selectionMode="single"
          dataKey="id"
          :loading="store.carregando"
          :paginator="filtradas.length > 10"
          :rows="10"
          class="!text-sm"
          :rowClass="(data) => solicitacaoSelecionada?.id === data.id ? '!bg-orange-50' : 'cursor-pointer'"
          @row-click="(event) => selecionar(event.data)"
        >
          <template #empty>
            <div class="flex flex-col items-center gap-2 py-10 text-zinc-400">
              <i class="pi pi-inbox text-3xl" />
              <span class="text-sm">Nenhuma solicitação encontrada</span>
            </div>
          </template>

          <Column field="id" header="ID" style="width: 70px">
            <template #body="{ data }">
              <span class="font-mono text-zinc-400">#{{ data.id }}</span>
            </template>
          </Column>

          <Column field="nome" header="Cliente">
            <template #body="{ data }">
              <div class="flex items-center gap-2">
                <Avatar
                  :label="iniciais(data.nome)"
                  shape="circle"
                  class="!w-7 !h-7 !text-xs !bg-orange-100 !text-orange-600 font-semibold"
                />
                <span class="font-medium text-zinc-800">{{ data.nome }}</span>
              </div>
            </template>
          </Column>

          <Column field="criado_em" header="Data">
            <template #body="{ data }">
              <div class="flex items-center gap-1.5 text-zinc-500">
                <i class="pi pi-calendar text-xs" />
                {{ formatDate(data.criado_em) }}
              </div>
            </template>
          </Column>

          <Column field="total" header="Total">
            <template #body="{ data }">
              <span class="font-semibold text-zinc-800">{{ preco(data.total) }}</span>
            </template>
          </Column>

          <Column field="status" header="Status">
            <template #body="{ data }">
              <Tag
                :value="infoStatus(data.status).label"
                :severity="infoStatus(data.status).severity"
                :icon="infoStatus(data.status).icon"
              />
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Painel de detalhes -->
      <div
        v-if="solicitacaoSelecionada"
        class="w-full lg:w-80 lg:shrink-0 bg-white border border-zinc-200 rounded-2xl p-5 space-y-4 shadow-sm"
        >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <i class="pi pi-file text-zinc-400" />
            <h3 class="font-bold text-zinc-900">#{{ solicitacaoSelecionada.id }}</h3>
          </div>
          <Tag
            :value="infoStatus(solicitacaoSelecionada.status).label"
            :severity="infoStatus(solicitacaoSelecionada.status).severity"
            :icon="infoStatus(solicitacaoSelecionada.status).icon"
          />
        </div>

        <div class="flex items-center gap-3">
          <Avatar
            :label="iniciais(solicitacaoSelecionada.nome)"
            shape="circle"
            class="!w-10 !h-10 !bg-orange-100 !text-orange-600 font-semibold"
          />
          <div class="text-sm space-y-0.5">
            <p class="font-semibold text-zinc-800">{{ solicitacaoSelecionada.nome }}</p>
            <p class="text-zinc-500 flex items-center gap-1.5">
              <i class="pi pi-phone text-xs" />
              {{ solicitacaoSelecionada.telefone }}
            </p>
          </div>
        </div>

        <div class="text-sm space-y-1.5">
          <p v-if="solicitacaoSelecionada.email" class="text-zinc-500 flex items-center gap-1.5">
            <i class="pi pi-envelope text-xs" />
            {{ solicitacaoSelecionada.email }}
          </p>
          <p v-if="endereco(solicitacaoSelecionada)" class="text-zinc-500 flex items-start gap-1.5">
            <i class="pi pi-map-marker text-xs mt-0.5" />
            <span>{{ endereco(solicitacaoSelecionada) }}</span>
          </p>
        </div>

        <Divider class="!my-1" />

        <div>
          <p class="text-xs font-semibold text-zinc-500 uppercase mb-2 flex items-center gap-1.5">
            <i class="pi pi-shopping-cart text-xs" />
            Itens
          </p>

          <div v-if="solicitacaoSelecionada.itens?.length">
            <div
              v-for="item in solicitacaoSelecionada.itens"
              :key="item.id ?? `${item.produto}-${item.quantidade}`"
              class="flex justify-between text-sm py-1.5 border-b border-zinc-100 last:border-0"
            >
              <span class="text-zinc-700">
                {{ item.produto_nome || 'Produto' }} x{{ item.quantidade }}
                <span v-if="item.variacao" class="text-zinc-400">({{ item.variacao }})</span>
              </span>
              <span class="font-semibold">{{ preco(item.subtotal) }}</span>
            </div>
          </div>

          <p v-else class="text-sm text-zinc-400 flex items-center gap-1.5 py-2">
            <i class="pi pi-info-circle" />
            Nenhum item encontrado.
          </p>

          <div class="flex justify-between font-bold text-zinc-900 mt-2 pt-2 border-t border-zinc-200">
            <span>Total</span>
            <span class="text-orange-500">{{ preco(solicitacaoSelecionada.total) }}</span>
          </div>
        </div>

        <div
          v-if="solicitacaoSelecionada.observacao"
          class="text-xs text-zinc-600 bg-zinc-50 rounded-xl p-3 flex gap-2"
        >
          <i class="pi pi-comment text-zinc-400 mt-0.5" />
          <span>{{ solicitacaoSelecionada.observacao }}</span>
        </div>

        <div>
          <p class="text-xs font-semibold text-zinc-500 uppercase mb-2">Alterar status</p>
          <Select
            :model-value="solicitacaoSelecionada.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecionar status"
            class="w-full !rounded-xl !text-sm"
            @update:model-value="(value) => changeStatus(solicitacaoSelecionada!.id, value)"
          >
            <template #value="{ value }">
              <div class="flex items-center gap-2">
                <i :class="infoStatus(value).icon" />
                <span>{{ infoStatus(value).label }}</span>
              </div>
            </template>
            <template #option="{ option }">
              <div class="flex items-center gap-2">
                <i :class="infoStatus(option.value).icon" />
                <span>{{ option.label }}</span>
              </div>
            </template>
          </Select>
        </div>

        <Button
          label="Responder no WhatsApp"
          icon="pi pi-whatsapp"
          class="w-full !bg-green-500 !border-green-500 hover:!bg-green-600 !rounded-xl"
          @click="abrirWhatsApp(solicitacaoSelecionada.telefone)"
        />
      </div>

    </div>
  </div>
</template>