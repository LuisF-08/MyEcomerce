<script setup lang="ts">
defineProps<{
  icon: string
  value: string | number
  label: string
  subLabel?: string
  color?: string
}>()
</script>

<template>
  <div class="bg-white border border-zinc-200 rounded-2xl p-6 flex items-start gap-4">
    <div
      :class="['w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0', color || 'bg-orange-100']"
    >
      <i :class="[icon, 'text-xl', color ? 'text-white' : 'text-orange-500']" />
    </div>
    <div>
      <p class="text-2xl font-bold text-zinc-900">{{ value }}</p>
      <p class="text-sm font-medium text-zinc-600">{{ label }}</p>
      <p v-if="subLabel" class="text-xs text-zinc-400 mt-0.5">{{ subLabel }}</p>
    </div>
  </div>
</template>
