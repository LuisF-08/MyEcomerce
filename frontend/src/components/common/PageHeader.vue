<script setup lang="ts">
defineProps<{
  icon: string
  title: string
  subtitle?: string
  badge?: string
}>()
</script>

<template>
  <header
    class="relative overflow-hidden rounded-2xl border border-zinc-200 dark:border-zinc-800
           bg-white dark:bg-zinc-900 shadow-sm p-4 sm:p-5"
  >
    <!-- barrinha de destaque  -->
    <span class="absolute left-0 top-1/2 -translate-y-1/2 h-10 w-[3px] rounded-full bg-orange-500" />

    <!-- brilho decorativo -->
    <div class="pointer-events-none absolute -top-12 -right-12 w-44 h-44 rounded-full bg-orange-500/10 blur-3xl" />

    <div class="relative flex flex-col sm:flex-row sm:items-center gap-4">
      <div class="flex items-center gap-3 sm:gap-4 min-w-0 flex-1">
        <div
          class="w-11 h-11 sm:w-12 sm:h-12 shrink-0 rounded-2xl bg-orange-500
                 flex items-center justify-center shadow-lg shadow-orange-500/20"
        >
          <i :class="[icon, 'text-white text-lg sm:text-xl']" />
        </div>

        <div class="min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <h2 class="text-lg sm:text-xl font-extrabold tracking-tight text-zinc-950 dark:text-white truncate">
              {{ title }}
            </h2>
            <span
              v-if="badge"
              class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-2.5 py-1 rounded-full
                     bg-orange-50 text-orange-600 ring-1 ring-orange-100
                     dark:bg-orange-500/10 dark:text-orange-400 dark:ring-orange-500/20"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-orange-500" />
              {{ badge }}
            </span>
          </div>
          <p v-if="subtitle" class="text-xs sm:text-sm text-zinc-900 dark:text-zinc-400 mt-0.5">
            {{ subtitle }}
          </p>
        </div>
      </div>

      <div v-if="$slots.actions" class="flex flex-wrap items-center gap-2 sm:shrink-0">
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>