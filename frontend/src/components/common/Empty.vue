<script setup lang="ts">
defineProps<{
  icon?: string
  title?: string
  description?: string
  actionLabel?: string
}>()

defineEmits<{ action: [] }>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 text-center">
    <div class="w-16 h-16 rounded-full bg-zinc-100 flex items-center justify-center mb-4">
      <i :class="[icon || 'pi pi-inbox', 'text-2xl text-zinc-400']" />
    </div>
    <h3 class="text-lg font-semibold text-zinc-800 mb-1">{{ title || 'Nenhum item encontrado' }}</h3>
    <p class="text-sm text-zinc-500 mb-4">{{ description || 'Tente ajustar os filtros ou adicione novos itens.' }}</p>
    <button
      v-if="actionLabel"
      class="px-4 py-2 bg-orange-500 text-white rounded-xl text-sm font-semibold hover:bg-orange-600 transition-colors"
      @click="$emit('action')"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>