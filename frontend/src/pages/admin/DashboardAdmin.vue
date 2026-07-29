<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

import { useDashboardStore } from '@/stores/dashboard'

import ResumoCard from '@/components/dashboard/ResumoCard.vue'
import GraficoPedidos from '@/components/dashboard/GraficoPedidos.vue'
import GraficoVendas from '@/components/dashboard/GraficoVendas.vue'
import UltimosPedidos from '@/components/dashboard/UltimosPedidos.vue'

const dashboard = useDashboardStore()
const router = useRouter()

const {
  dados,
  carregando,
  erro
} = storeToRefs(dashboard)

onMounted(() => {
  dashboard.carregarDashboard()
})

function formatarMoeda(valor: number) {
  return valor.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

const faturamentoFormatado = computed(() =>
  formatarMoeda(
    dados.value?.cards.faturamento ?? 0
  )
)

// O service (`DashboardService.obter_cards_gerais`) manda a chave
// `produto_medio`, não `ticket_medio` — usando o nome real que a API
// devolve pra não ficar sempre 0. Se preferir manter `ticket_medio`
// no front, é só renomear a chave lá no service.
const ticketMedioFormatado = computed(() =>
  formatarMoeda(
    dados.value?.cards.produto_medio ?? 0
  )
)
</script>

<template>

  <div class="space-y-4 sm:space-y-6 p-4 sm:p-6">

    <!-- Carregando -->
    <div
      v-if="carregando"
      class="flex items-center justify-center py-16 sm:py-20"
    >
      <i
        class="pi pi-spin pi-spinner text-3xl text-orange-500"
      />
    </div>


    <!-- Erro -->
    <div
      v-else-if="erro"
      class="bg-red-50 dark:bg-red-500/10
             border border-red-200 dark:border-red-500/30
             rounded-2xl p-4 sm:p-6 text-sm
             text-red-600 dark:text-red-400"
    >
      {{ erro }}
    </div>


    <!-- Dashboard -->
    <template v-else-if="dados">

      <!-- Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">

        <ResumoCard
          icon="pi pi-dollar"
          :value="faturamentoFormatado"
          label="Faturamento"
          sub-label="total"
          color="bg-emerald-100 dark:bg-emerald-500/10"
          accent-color="border-l-emerald-500 dark:border-l-emerald-400"
        />

        <ResumoCard
          icon="pi pi-bell"
          :value="dados.cards.pedidos_novos"
          label="Pedidos novos"
          sub-label="aguardando"
          color="bg-blue-100 dark:bg-blue-500/10"
          accent-color="border-l-blue-500 dark:border-l-blue-400"
        />

        <ResumoCard
          icon="pi pi-shopping-cart"
          :value="dados.cards.total_pedidos"
          label="Pedidos"
          sub-label="total"
          accent-color="border-l-orange-500 dark:border-l-orange-400"
        />

        <ResumoCard
            icon="pi pi-chart-line"
            :value="ticketMedioFormatado"
            label="Ticket médio"
            sub-label="por pedido"
            color="bg-purple-100 dark:bg-purple-500/10"
            accent-color="border-l-purple-500 dark:border-l-purple-400"
        />

      </div>


      <!-- Gráficos -->
      <div class="grid md:grid-cols-2 gap-4 sm:gap-6">

        <GraficoPedidos />
        <GraficoVendas />

      </div>

      <div class="w-full">
        <UltimosPedidos />
      </div>


      <!-- Ações rápidas -->
      <div
        class="bg-white dark:bg-zinc-900
               border border-zinc-200 dark:border-zinc-800
               rounded-2xl p-4 sm:p-6"
      >

        <h3
          class="text-sm font-semibold
                 text-zinc-500 dark:text-zinc-400
                 uppercase tracking-wide mb-3 sm:mb-4"
        >
          Ações rápidas
        </h3>

        <div class="flex flex-col sm:flex-row sm:flex-wrap gap-2.5 sm:gap-3">

          <button
            class="w-full sm:w-auto justify-center px-4 py-2.5 sm:py-2 bg-orange-500 text-white
                   rounded-xl text-sm font-semibold
                   hover:bg-orange-600 transition-colors
                   flex items-center gap-2"
            @click="router.push({ name: 'admin-produtos' })"
          >
            <i class="pi pi-plus" />
            Novo produto
          </button>

          <button
            class="w-full sm:w-auto justify-center px-4 py-2.5 sm:py-2 border border-zinc-200
                   dark:border-zinc-700
                   text-zinc-700 dark:text-zinc-300
                   rounded-xl text-sm font-semibold
                   hover:bg-zinc-50 dark:hover:bg-zinc-800
                   transition-colors
                   flex items-center gap-2"
            @click="router.push({ name: 'admin-solicitacoes' })"
          >
            <i class="pi pi-list-check" />
            Ver solicitações
          </button>

          <button
            class="w-full sm:w-auto justify-center px-4 py-2.5 sm:py-2 border border-zinc-200
                   dark:border-zinc-700
                   text-zinc-700 dark:text-zinc-300
                   rounded-xl text-sm font-semibold
                   hover:bg-zinc-50 dark:hover:bg-zinc-800
                   transition-colors
                   flex items-center gap-2"
            @click="router.push({ name: 'home' })"
          >
            <i class="pi pi-external-link" />
            Ver loja
          </button>

          <button
            class="w-full sm:w-auto justify-center px-4 py-2.5 sm:py-2 border border-zinc-200
                   dark:border-zinc-700
                   text-zinc-700 dark:text-zinc-300
                   rounded-xl text-sm font-semibold
                   hover:bg-zinc-50 dark:hover:bg-zinc-800
                   transition-colors
                   flex items-center gap-2"
            @click="dashboard.baixarRelatorioCSV"
          >
            <i class="pi pi-file-export" />
            Exportar relatório
          </button>

        </div>

      </div>

    </template>

  </div>

</template>