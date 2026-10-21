<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  icon: string
  value: string | number
  label: string
  subLabel?: string
  color?: string
  accentColor?: string
}

const props = withDefaults(defineProps<Props>(), {
  subLabel: undefined,
  color: undefined,
  accentColor: undefined,
})

const bgClass = computed(() => props.color || 'bg-orange-100 dark:bg-orange-500/10')
const iconClass = computed(() => (props.color ? 'text-white' : 'text-orange-500 dark:text-orange-400'))
const accentClass = computed(() => props.accentColor || 'border-l-orange-500 dark:border-l-orange-400')
</script>

<template>
  <div
    :class="[
      'bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 border-l-4 rounded-2xl',
      'p-3 sm:p-6 flex items-start gap-3 sm:gap-4 min-w-0',
      accentClass,
    ]"
  >
    <div :class="['w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center shrink-0', bgClass]">
      <i :class="[icon, 'text-lg sm:text-xl text-zinc-900 dark:text-zinc-200', iconClass]" />
    </div>
    <div class="min-w-0">
      <p class="text-lg sm:text-2xl font-bold text-zinc-900 dark:text-zinc-50 truncate">{{ value }}</p>
      <p class="text-xs sm:text-sm font-medium text-zinc-600 dark:text-zinc-400 truncate">{{ label }}</p>
      <p v-if="subLabel" class="text-[11px] sm:text-xs text-zinc-700 dark:text-zinc-500 mt-0.5 truncate">{{ subLabel }}</p>
    </div>
  </div>
</template>