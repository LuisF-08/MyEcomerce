<script setup lang="ts">
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useLojaStore } from "@/stores/loja"
import Depoiments from "@/components/layout/Depoiments.vue"
import { diasLabel, formatarHora, lojaAberta, whatsappLink } from "@/utils/loja"

const lojaStore = useLojaStore()
const { loja } = storeToRefs(lojaStore)

const aberta = computed(() => lojaAberta(loja.value))

const formatarData = (data: string | undefined) => {
  if (!data) return 'Data não disponível'
  return new Date(data).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-16">

    <!-- Header -->
    <div class="text-center mb-14">
      <span class="inline-flex items-center gap-2 bg-orange-50 dark:bg-orange-500/10 text-orange-600 dark:text-orange-400 text-xs font-semibold px-4 py-1.5 rounded-full mb-4 ring-1 ring-orange-100 dark:ring-orange-500/20">
        <i class="pi pi-heart-fill text-[10px]" />
        Nossa história
      </span>
      <h1 class="text-4xl font-extrabold text-zinc-900 dark:text-white mb-3 tracking-tight">Sobre nós</h1>
      <p class="text-zinc-500 dark:text-zinc-400 text-lg max-w-xl mx-auto">
        Criado em <span class="text-zinc-700 dark:text-zinc-200 font-medium">{{ formatarData(loja?.criado_em) }}</span>,
        conheça a nossa história e o que nos motiva.
      </p>
    </div>

    <!-- Story + Image -->
    <div class="grid md:grid-cols-2 gap-10 items-center mb-16">
      <div>
        <h2 class="text-xl font-bold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
          <span class="w-1.5 h-6 bg-orange-500 rounded-full" />
          Quem somos
        </h2>
        <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-sm mb-4">{{ loja?.descricao }}</p>
        <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-sm mb-4">
          Nascemos da vontade de facilitar o comércio local, conectando pequenos lojistas com seus clientes
          de forma simples e eficiente. Nosso catálogo digital permite que você explore produtos e faça pedidos
          diretamente pelo WhatsApp — sem complicações.
        </p>
        <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-sm">
          Acreditamos que o comércio local tem um papel fundamental na economia e na vida das comunidades.
          Por isso, trabalhamos para oferecer as melhores ferramentas para quem vende com paixão.
        </p>
      </div>

      <div class="relative">
        <div class="absolute -inset-3 bg-gradient-to-br from-orange-200 via-orange-100 to-transparent dark:from-orange-500/20 dark:via-orange-500/5 dark:to-transparent rounded-3xl blur-xl opacity-70" />
        <div class="relative rounded-2xl overflow-hidden aspect-square shadow-lg ring-1 ring-black/5 dark:ring-white/10">
          <img
            src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=600&fit=crop&auto=format"
            alt="Nossa loja"
            class="w-full h-full object-cover"
          />
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-5 mb-16">
      <div
        v-for="s in [
          { value: '500+', label: 'Clientes atendidos', icon: 'pi-users' },
          { value: '8', label: 'Categorias', icon: 'pi-th-large' },
          { value: '50+', label: 'Produtos', icon: 'pi-box' },
          { value: '4.9★', label: 'Avaliação média', icon: 'pi-star-fill' },
        ]"
        :key="s.label"
        class="bg-gradient-to-b from-white to-orange-50/40 dark:from-zinc-900 dark:to-zinc-900/60 border border-orange-100 dark:border-zinc-800 rounded-2xl p-5 text-center hover:shadow-md dark:hover:border-orange-500/30 hover:-translate-y-0.5 transition-all duration-200"
      >
        <i :class="['pi', s.icon, 'text-orange-400 text-lg mb-2']" />
        <p class="text-2xl font-extrabold text-orange-500 dark:text-orange-400 mb-1">{{ s.value }}</p>
        <p class="text-xs text-zinc-500 dark:text-zinc-400 font-medium">{{ s.label }}</p>
      </div>
    </div>

    <Depoiments />

    <!-- Contact card -->
    <div
      class="group relative overflow-hidden rounded-3xl p-6 sm:p-10
             text-zinc-900 dark:text-white
             bg-gradient-to-br from-orange-50 via-white to-amber-50
             dark:from-zinc-900 dark:via-zinc-950 dark:to-black
             ring-1 ring-orange-200/70 dark:ring-white/10
             shadow-xl shadow-orange-500/10 dark:shadow-2xl dark:shadow-black/30 mt-12"
    >
      <!-- Brilho que atravessa o card no hover -->
      <div class="absolute inset-0 -translate-x-full group-hover:translate-x-full duration-1000 bg-gradient-to-r from-transparent via-orange-300/30 dark:via-white/10 to-transparent transform pointer-events-none transition-transform ease-in-out z-0" />

      <!-- Linha de luz no topo -->
      <div class="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-orange-400/70 dark:via-amber-400/60 to-transparent pointer-events-none" />

      <!-- Orbes decorativos -->
      <div class="absolute -top-20 -right-20 w-64 h-64 bg-orange-400/20 dark:bg-amber-500/15 rounded-full blur-3xl pointer-events-none" />
      <div class="absolute -bottom-24 -left-16 w-60 h-60 bg-amber-300/20 dark:bg-amber-400/10 rounded-full blur-3xl pointer-events-none" />
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.6),transparent_60%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.05),transparent_60%)] pointer-events-none" />

      <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-8">

        <!-- Texto -->
        <div class="min-w-0">
          <span
            v-if="loja"
            class="inline-flex items-center gap-2 text-xs font-semibold px-3 py-1 rounded-full mb-4 ring-1"
            :class="aberta
              ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 ring-emerald-500/30 dark:ring-emerald-500/20'
              : 'bg-red-500/10 text-red-700 dark:text-red-400 ring-red-500/30 dark:ring-red-500/20'"
          >
            <span class="w-1.5 h-1.5 rounded-full" :class="aberta ? 'bg-emerald-500 dark:bg-emerald-400 animate-pulse' : 'bg-red-500 dark:bg-red-400'" />
            {{ aberta ? 'Aberto agora' : 'Fechado no momento' }}
          </span>

          <h3 class="text-2xl sm:text-3xl font-extrabold tracking-tight flex items-center gap-2 text-zinc-900 dark:text-white">
            Fale com a gente!
          </h3>
          <p class="text-zinc-600 dark:text-zinc-400 text-sm mt-1.5">
            Estamos disponíveis de {{ diasLabel(loja?.dias_funcionamento).toLowerCase() }}.
          </p>

          <div class="mt-6 grid sm:grid-cols-2 gap-3">
            <div class="flex items-start gap-3 rounded-2xl bg-white/80 dark:bg-white/5 ring-1 ring-orange-100 dark:ring-white/10 p-4 backdrop-blur-sm shadow-sm dark:shadow-none">
              <span class="w-9 h-9 shrink-0 rounded-xl bg-orange-100 dark:bg-amber-400/10 ring-1 ring-orange-200 dark:ring-amber-400/20 flex items-center justify-center">
                <i class="pi pi-map-marker text-orange-600 dark:text-amber-400 text-sm" />
              </span>
              <div class="min-w-0 text-sm">
                <p class="text-[11px] font-bold uppercase tracking-wider text-zinc-500">Endereço</p>
                <p class="text-zinc-700 dark:text-zinc-300 mt-0.5 leading-snug">
                  {{ loja?.rua }}, {{ loja?.numero }}<span v-if="loja?.bairro"> - {{ loja.bairro }}</span><br />
                  {{ loja?.cidade }}/{{ loja?.estado }}<span v-if="loja?.cep"> · {{ loja.cep }}</span>
                </p>
              </div>
            </div>

            <div class="flex items-start gap-3 rounded-2xl bg-white/80 dark:bg-white/5 ring-1 ring-orange-100 dark:ring-white/10 p-4 backdrop-blur-sm shadow-sm dark:shadow-none">
              <span class="w-9 h-9 shrink-0 rounded-xl bg-orange-100 dark:bg-amber-400/10 ring-1 ring-orange-200 dark:ring-amber-400/20 flex items-center justify-center">
                <i class="pi pi-clock text-orange-600 dark:text-amber-400 text-sm" />
              </span>
              <div class="min-w-0 text-sm">
                <p class="text-[11px] font-bold uppercase tracking-wider text-zinc-500">Horário</p>
                <p class="text-zinc-700 dark:text-zinc-300 mt-0.5 leading-snug">
                  {{ diasLabel(loja?.dias_funcionamento) }}<br />
                  {{ formatarHora(loja?.horario_funcionamento) }} às {{ formatarHora(loja?.horario_fechamento) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Botão WhatsApp com cor do ícone corrigida -->
        <a
          :href="whatsappLink(loja, loja?.mensagem_whatsapp)"
          target="_blank"
          rel="noopener"
          class="group/btn inline-flex items-center justify-center gap-3 px-7 py-4 rounded-2xl shrink-0
                 bg-gradient-to-b from-green-400 to-green-600 text-white font-bold text-sm no-underline
                 shadow-lg shadow-green-500/25 ring-1 ring-white/20
                 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-2xl hover:shadow-green-900/40 active:scale-95"
        >
          <i class="pi pi-whatsapp text-xl transition-colors duration-200 group-hover/btn:text-yellow-300" />
          Falar no WhatsApp
          <i class="pi pi-arrow-right text-xs transition-transform duration-300 group-hover/btn:translate-x-1" />
        </a>
      </div>
    </div>

  </div>
</template>