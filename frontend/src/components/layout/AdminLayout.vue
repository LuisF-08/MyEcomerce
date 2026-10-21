<script setup lang="ts">
import { ref } from "vue"
import { RouterView } from "vue-router"
import Toast from "primevue/toast"
import Sidebar from "@/components/layout/Sidebar.vue"

const menuMobileAberto = ref(false)
</script>

<template>
  <div class="flex h-dvh overflow-hidden">
    <Sidebar
      :mobile-open="menuMobileAberto"
      @close="menuMobileAberto = false"
    />

    <main class="flex-1 min-w-0 overflow-y-auto">
      <Toast />

      <!-- Barra superior (apenas mobile) -->
      <div
        class="md:hidden sticky top-0 z-30 h-14 px-4 flex items-center gap-3
               bg-white/95 dark:bg-zinc-950/95 backdrop-blur-sm
               border-b border-zinc-100 dark:border-zinc-800/60"
      >
        <button
          type="button"
          class="w-10 h-10 flex items-center justify-center rounded-full
                 text-zinc-600 dark:text-zinc-300
                 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-colors"
          aria-label="Abrir menu"
          @click="menuMobileAberto = true"
        >
          <i class="pi pi-bars text-xl" />
        </button>
        <span class="font-bold text-zinc-950 dark:text-white tracking-tight">
          Catálogo<span class="text-orange-500">.</span>
        </span>
      </div>

      <RouterView />
    </main>
  </div>
</template>