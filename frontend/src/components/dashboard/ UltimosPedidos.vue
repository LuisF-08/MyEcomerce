<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import { getSolicitacoes } from '@/services/solicitacao'
import type { Solicitacao } from '@/types/solicitacao'

const pedidos = ref<Solicitacao[]>([])

onMounted(async () => {
  const all = await getSolicitacoes()
  pedidos.value = all.slice(0, 5)
})

const statusSeverity = (status: string) => {
  const map: Record<string, string> = {
    Novo: 'info',
    Visto: 'warn',
    'Concluído': 'success',
    Cancelado: 'danger',
  }
  return map[status] || 'secondary'
}

const preco = (v: number) => `R$ ${v.toFixed(2).replace('.', ',')}`
</script>

<template>
  <div class="bg-white border border-zinc-200 rounded-2xl overflow-hidden">
    <div class="px-6 py-4 border-b border-zinc-100">
      <h3 class="text-sm font-semibold text-zinc-500 uppercase tracking-wide">Últimas solicitações</h3>
    </div>
    <DataTable :value="pedidos" class="!text-sm">
      <Column field="id" header="ID" style="width: 80px" />
      <Column field="cliente" header="Cliente" />
      <Column field="total" header="Total">
        <template #body="{ data }">{{ preco(data.total) }}</template>
      </Column>
      <Column field="status" header="Status">
        <template #body="{ data }">
          <Tag :value="data.status" :severity="statusSeverity(data.status)" />
        </template>
      </Column>
    </DataTable>
  </div>
</template>
