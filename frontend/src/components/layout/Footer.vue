<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { storeToRefs } from 'pinia'

import { useLojaStore } from '@/stores/loja'
import { useCategoriaStore } from '@/stores/categoria'
import { useCarrinhoStore } from '@/stores/carrinho'
import BrandLogo from '@/components/common/BrandLogo.vue'
import { diasLabel, formatarHora, lojaAberta, whatsappLink } from '@/utils/loja'

const { loja } = storeToRefs(useLojaStore())
const categoriaStore = useCategoriaStore()
const carrinho = useCarrinhoStore()

const categorias = computed(() => categoriaStore.categorias.filter((c) => c.ativo).slice(0, 6))
const aberta = computed(() => lojaAberta(loja.value))
const carregada = computed(() => !!loja.value)
const telefoneLink = computed(() => `tel:${(loja.value?.telefone ?? '').replace(/\D/g, '')}`)
const ano = new Date().getFullYear()

function voltarAoTopo() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <footer class="relative bg-zinc-100 dark:bg-zinc-950 rounded-3xl text-zinc-600 dark:text-zinc-400 
  mt-16 overflow-hidden border-t border-zinc-200 dark:border-transparent">
    <div class="pointer-events-none absolute -top-32 left-1/2 -translate-x-1/2 w-[40rem] h-64 rounded-full bg-orange-500/10 blur-3xl" />

    <div class="relative max-w-6xl mx-auto px-4 pt-12 sm:pt-16">

      <!-- Faixa de chamada -->
      <div
  class="rounded-3xl p-6 sm:p-8 flex flex-col md:flex-row md:items-center justify-between gap-5
          bg-gradient-to-br from-orange-500 to-orange-700 text-white shadow-xl shadow-orange-500/15
          relative overflow-hidden group"
        >
  <!-- Efeito de brilho ajustado para cruzar o card de lado a lado -->
    <div class="absolute inset-0 -translate-x-full group-hover:translate-x-full duration-1000 bg-gradient-to-r from-transparent via-white/30 to-transparent transform pointer-events-none transition-transform ease-in-out"></div>
    
      <div class="relative z-10">
        <h3 class="text-xl sm:text-2xl font-extrabold tracking-tight">Ficou com alguma dúvida?</h3>
        <p class="text-white/85 text-sm mt-1">Chame a gente no WhatsApp e faça seu pedido sem complicação.</p>
      </div>
    
      <a
        :href="whatsappLink(loja, loja?.mensagem_whatsapp)"
        target="_blank"
        rel="noopener"
        class="relative z-10 inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-white text-zinc-900
                font-bold text-sm shadow-lg transition-all duration-300 
                hover:bg-green-600 hover:text-white
                hover:-translate-y-0.5 hover:shadow-2xl hover:shadow-green-900/30 active:scale-95 no-underline
                group/btn"
      >
        <i class="pi pi-whatsapp text-green-500 group-hover/btn:text-yellow-300 text-lg transition-colors duration-200" />
        Falar no WhatsApp
      </a>
    </div>

      <!-- Colunas -->
      <div class="grid grid-cols-2 md:grid-cols-12 gap-8 md:gap-6 py-12">

        <div class="col-span-2 md:col-span-4">
          <BrandLogo size="md" />
          <p class="text-sm leading-relaxed mt-4 max-w-xs">
            {{ loja?.descricao || 'Sua loja digital para comprar com praticidade e atendimento direto pelo WhatsApp.' }}
          </p>

          <div class="flex gap-2.5 mt-5">
            <a v-if="loja?.instagram" :href="loja.instagram" target="_blank" rel="noopener" aria-label="Instagram"
               class="w-10 h-10 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-zinc-600 dark:text-zinc-300 transition-all hover:bg-orange-500 hover:border-orange-500 hover:text-white hover:-translate-y-0.5">
              <i class="pi pi-instagram" />
            </a>
            <a v-if="loja?.facebook" :href="loja.facebook" target="_blank" rel="noopener" aria-label="Facebook"
               class="w-10 h-10 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-zinc-600 dark:text-zinc-300 transition-all hover:bg-blue-600 hover:border-blue-600 hover:text-white hover:-translate-y-0.5">
              <i class="pi pi-facebook" />
            </a>
            <a :href="whatsappLink(loja)" target="_blank" rel="noopener" aria-label="WhatsApp"
               class="w-10 h-10 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 flex items-center justify-center text-zinc-600 dark:text-zinc-300 transition-all hover:bg-green-500 hover:border-green-500 hover:text-white hover:-translate-y-0.5">
              <i class="pi pi-whatsapp" />
            </a>
          </div>
        </div>

        <div class="md:col-span-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-zinc-900 dark:text-white mb-4">Navegação</h4>
          <ul class="space-y-2.5 text-sm">
            <li><RouterLink :to="{ name: 'home' }" class="no-underline text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors">Início</RouterLink></li>
            <li><RouterLink :to="{ name: 'produtos' }" class="no-underline text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors">Produtos</RouterLink></li>
            <li><RouterLink :to="{ name: 'sobre' }" class="no-underline text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors">Sobre nós</RouterLink></li>
            <li>
              <button type="button" class="text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors" @click="carrinho.abrir()">
                Meu carrinho
                <span v-if="carrinho.quantidadeItens" class="ml-1 text-xs font-bold text-orange-500 dark:text-orange-400">({{ carrinho.quantidadeItens }})</span>
              </button>
            </li>
          </ul>
        </div>

        <div class="md:col-span-2">
          <h4 class="text-xs font-bold uppercase tracking-wider text-zinc-900 dark:text-white mb-4">Categorias</h4>
          <ul v-if="categorias.length" class="space-y-2.5 text-sm">
            <li v-for="c in categorias" :key="c.id">
              <RouterLink :to="{ name: 'produtos', query: { categoria: String(c.id) } }"
                          class="no-underline text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors">
                {{ c.nome }}
              </RouterLink>
            </li>
          </ul>
          <p v-else class="text-sm text-zinc-400 dark:text-zinc-600">Em breve</p>
        </div>

        <div class="col-span-2 md:col-span-4">
          <h4 class="text-xs font-bold uppercase tracking-wider text-zinc-900 dark:text-white mb-4">Atendimento</h4>

          <span
            v-if="carregada"
            class="inline-flex items-center gap-2 text-xs font-semibold px-3 py-1 rounded-full mb-4"
            :class="aberta
              ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 ring-1 ring-emerald-500/20'
              : 'bg-red-500/10 text-red-600 dark:text-red-400 ring-1 ring-red-500/20'"
          >
            <span class="w-1.5 h-1.5 rounded-full" :class="aberta ? 'bg-emerald-500 dark:bg-emerald-400 animate-pulse' : 'bg-red-500 dark:bg-red-400'" />
            {{ aberta ? 'Aberto agora' : 'Fechado no momento' }}
          </span>

          <ul class="space-y-3 text-sm">
            <li class="flex items-start gap-3">
              <i class="pi pi-clock text-orange-500 dark:text-orange-400 mt-0.5" />
              <span>
                {{ diasLabel(loja?.dias_funcionamento) }}<br />
                {{ formatarHora(loja?.horario_funcionamento) }} às {{ formatarHora(loja?.horario_fechamento) }}
              </span>
            </li>
            <li class="flex items-start gap-3">
              <i class="pi pi-map-marker text-orange-500 dark:text-orange-400 mt-0.5" />
              <span>
                {{ loja?.rua }}, {{ loja?.numero }}<span v-if="loja?.bairro"> - {{ loja.bairro }}</span><br />
                {{ loja?.cidade }}/{{ loja?.estado }}<span v-if="loja?.cep"> · CEP {{ loja.cep }}</span>
              </span>
            </li>
            <li v-if="loja?.telefone" class="flex items-center gap-3">
              <i class="pi pi-phone text-orange-500 dark:text-orange-400" />
              <a :href="telefoneLink" class="text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors no-underline">{{ loja.telefone }}</a>
            </li>
            <li v-if="loja?.email" class="flex items-center gap-3 min-w-0">
              <i class="pi pi-envelope text-orange-500 dark:text-orange-400" />
              <a :href="`mailto:${loja.email}`" class="text-zinc-600 dark:text-zinc-400 hover:text-orange-600 dark:hover:text-white transition-colors no-underline truncate">{{ loja.email }}</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Pagamento e segurança -->
      <div class="border-t border-zinc-200 dark:border-zinc-800/80 py-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-zinc-500 mr-1">Pagamento</span>
          <span v-if="loja?.pix" class="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300">
            <i class="pi pi-qrcode text-orange-500 dark:text-orange-400" /> Pix
          </span>
          <span class="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300">
            <i class="pi pi-credit-card text-orange-500 dark:text-orange-400" /> Cartão
          </span>
          <span class="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300">
            <i class="pi pi-wallet text-orange-500 dark:text-orange-400" /> Mercado Pago
          </span>
        </div>

        <span class="inline-flex items-center gap-2 text-xs text-zinc-500">
          <i class="pi pi-lock text-emerald-500 dark:text-emerald-400" />
          Pagamento processado em ambiente seguro. Não guardamos dados de cartão.
        </span>
      </div>

      <!-- Copyright centralizado -->
      <div class="border-t border-zinc-200 dark:border-zinc-800/80 py-5 text-center text-xs text-zinc-500">
        © {{ ano }} {{ loja?.nome }}. Todos os direitos reservados.
        <span v-if="loja?.cnpj"> · CNPJ {{ loja.cnpj }}</span>
      </div>
    </div>
  </footer>
</template>