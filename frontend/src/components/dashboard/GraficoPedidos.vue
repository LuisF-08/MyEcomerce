<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
} from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip)

const canvas = ref<HTMLCanvasElement>()

onMounted(() => {
  if (!canvas.value) return
  new Chart(canvas.value, {
    type: 'bar',
    data: {
      labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
      datasets: [
        {
          data: [4, 7, 3, 9, 6, 2, 1],
          backgroundColor: '#f97316',
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f4f4f5' } },
        x: { grid: { display: false } },
      },
    },
  })
})
</script>

<template>
  <div class="bg-white border border-zinc-200 rounded-2xl p-6">
    <h3 class="text-sm font-semibold text-zinc-500 uppercase tracking-wide mb-4">Pedidos por dia</h3>
    <canvas ref="canvas" />
  </div>
</template>
