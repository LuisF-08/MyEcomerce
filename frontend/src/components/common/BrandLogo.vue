<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useLojaStore } from '@/stores/loja'
import { resolveMediaUrl } from '@/config/api'

const props = withDefaults(
  defineProps<{
    size?: 'sm' | 'md' | 'lg'
    showName?: boolean
    inverted?: boolean // texto branco (para fundos escuros, ex.: footer)
  }>(),
  { size: 'md', showName: true, inverted: false },
)

const { loja } = storeToRefs(useLojaStore())

const caixa = computed(
  () =>
    ({
      sm: 'w-8 h-8 rounded-xl',
      md: 'w-10 h-10 rounded-2xl',
      lg: 'w-14 h-14 rounded-2xl',
    })[props.size],
)

const texto = computed(
  () => ({ sm: 'text-base', md: 'text-lg sm:text-xl', lg: 'text-2xl' })[props.size],
)
</script>

<template>
  <span class="inline-flex items-center gap-2.5 min-w-0">
    <!-- Logo enviada pela loja -->
    <img
      v-if="loja?.logo"
      :src="resolveMediaUrl(loja.logo)"
      :alt="loja.nome"
      class="shrink-0 object-cover shadow-lg shadow-orange-500/20 ring-1 ring-black/5"
      :class="caixa"
    />

    <!-- Marca padrão -->
    <span
      v-else
      class="relative shrink-0 flex items-center justify-center
             bg-gradient-to-br from-orange-400 via-orange-500 to-orange-600
             shadow-lg shadow-orange-500/30 ring-1 ring-white/20"
      :class="caixa"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.8"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="w-[58%] h-[58%] text-white drop-shadow-sm"
        aria-hidden="true"
      >
        <path d="M5.5 8.5h13l-1 11a1.5 1.5 0 0 1-1.5 1.4H8a1.5 1.5 0 0 1-1.5-1.4l-1-11Z" />
        <path d="M9 8.5V7a3 3 0 0 1 6 0v1.5" />
        <path d="M9.5 13.5c.6 1.1 1.5 1.7 2.5 1.7s1.9-.6 2.5-1.7" />
      </svg>
    </span>

    <span
      v-if="showName"
      class="font-extrabold tracking-tight truncate max-w-[9rem] sm:max-w-[16rem]"
      :class="[texto, inverted ? 'text-white' : 'text-zinc-950 dark:text-white']"
    >
      {{ loja?.nome || 'Minha Loja' }}<span class="text-orange-500">.</span>
    </span>
  </span>
</template>