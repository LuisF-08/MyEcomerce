<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Categoria } from '@/types/categoria'
import { resolveMediaUrl } from '@/config/api'

const props = defineProps<{ categoria: Categoria }>()
const router = useRouter()

const imagemQuebrada = ref(false)
const imagem = computed(() =>
  props.categoria.imagem && !imagemQuebrada.value ? resolveMediaUrl(props.categoria.imagem) : '',
)

function abrir() {
  router.push({ name: 'produtos', query: { categoria: String(props.categoria.id) } })
}
</script>

<template>
  <button
    type="button"
    class="group relative flex items-center gap-3 w-full text-left overflow-hidden rounded-2xl p-3 pr-4
           bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm
           transition-all duration-300 ease-out
           hover:-translate-y-1 hover:shadow-lg hover:shadow-orange-500/15
           hover:border-orange-300 dark:hover:border-orange-500/40
           active:scale-[0.97] active:shadow-sm"
    @click="abrir"
  >
    <!-- filete que cresce no hover -->
    <span
      class="pointer-events-none absolute inset-y-0 left-0 w-1 bg-orange-500 origin-center scale-y-0
             transition-transform duration-300 group-hover:scale-y-100"
    />

    <!-- ícone / foto -->
    <span
      class="relative w-12 h-12 shrink-0 rounded-xl overflow-hidden flex items-center justify-center
             bg-orange-50 dark:bg-orange-500/10 ring-1 ring-orange-100 dark:ring-orange-500/20
             transition-transform duration-300 group-hover:scale-105 group-hover:-rotate-3"
    >
      <img
        v-if="imagem"
        :src="imagem"
        :alt="categoria.nome"
        loading="lazy"
        class="w-full h-full object-cover"
        @error="imagemQuebrada = true"
      />
      <i v-else class="pi pi-tag text-orange-500 text-lg" />
    </span>

    <!-- texto -->
    <span class="min-w-0 flex-1">
      <span
        class="block font-bold text-sm text-zinc-800 dark:text-zinc-100 truncate
               transition-colors group-hover:text-orange-600 dark:group-hover:text-orange-400"
      >
        {{ categoria.nome }}
      </span>
      <span v-if="categoria.descricao" class="block text-xs text-zinc-500 dark:text-zinc-400 truncate mt-0.5">
        {{ categoria.descricao }}
      </span>
    </span>

    <i
      class="pi pi-arrow-right text-xs text-zinc-300 dark:text-zinc-600 transition-all duration-300
             group-hover:text-orange-500 group-hover:translate-x-1"
    />
  </button>
</template>