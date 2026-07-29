import { defineStore } from 'pinia'
import { ref } from 'vue'

import { exportarRelatorioCSV,dashboard as buscarDashboard } from '@/services/dashboard'

import type {
    DashboardResponse
} from '@/types/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {

    const dados = ref<DashboardResponse | null>(null)

    const carregando = ref(false)

    const erro = ref<string | null>(null)

    async function carregarDashboard() {

    carregando.value = true
    erro.value = null

    try {

      dados.value = await buscarDashboard()

    } catch (error) {

      console.error(
        'Erro ao carregar dashboard:',
        error
      )

      erro.value =
        'Não foi possível carregar os dados do dashboard.'

    } finally {

      carregando.value = false

    }
  }
  async function baixarRelatorioCSV() {
    try {
      const blob = await exportarRelatorioCSV()
  
      const url = window.URL.createObjectURL(blob)
  
      const link = document.createElement('a')
      link.href = url
      link.download = 'relatorio_solicitacoes.csv'
  
      document.body.appendChild(link)
      link.click()
  
      link.remove()
      window.URL.revokeObjectURL(url)
  
    } catch (error) {
      console.error('Erro ao exportar relatório:', error)
  
      erro.value = 'Não foi possível exportar o relatório.'
    }
  }

  return {
    dados,
    carregando,
    erro,
    carregarDashboard,
    baixarRelatorioCSV
  }
})

