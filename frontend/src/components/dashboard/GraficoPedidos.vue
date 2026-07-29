```vue
<script setup lang="ts">
import { computed, onMounted } from 'vue'
import Chart from 'primevue/chart'
import { useDashboardStore } from '@/stores/dashboard'

const dashboard = useDashboardStore()

onMounted(() => {
  if (!dashboard.dados) {
    dashboard.carregarDashboard()
  }
})

const chartData = computed(() => {
  const dados = dashboard.dados?.grafico_pedidos ?? []

  return {
    labels: dados.map(item => item.mes),

    datasets: [
      {
        label: 'Pedidos',
        data: dados.map(item => item.quantidade),
        tension: 0.4,
        fill: false
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: true
    }
  },

  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0
      }
    }
  }
}
</script>

<template>
  <div class="bg-white dark:bg-zinc-900 rounded-2xl p-6 shadow-sm">

    <div class="mb-6">
      <h2 class="text-lg font-bold text-zinc-900 dark:text-white">
        Pedidos por mês
      </h2>

      <p class="text-sm text-zinc-500 dark:text-zinc-400">
        Evolução dos pedidos concluídos
      </p>
    </div>

    <div
      v-if="dashboard.carregando"
      class="h-80 flex items-center justify-center"
    >
      <i class="pi pi-spin pi-spinner text-2xl text-orange-500" />
    </div>

    <div
      v-else-if="!dashboard.dados?.grafico_pedidos?.length"
      class="h-80 flex items-center justify-center text-zinc-400"
    >
      Nenhum pedido concluído ainda.
    </div>

    <div
      v-else
      class="h-80"
    >
      <Chart
        type="line"
        :data="chartData"
        :options="chartOptions"
        class="w-full h-full"
      />
    </div>

  </div>
</template>
```
