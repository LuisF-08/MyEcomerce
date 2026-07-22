<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { icon: 'pi pi-chart-bar', label: 'Dashboard', to: '/admin/dashboard' },
  { icon: 'pi pi-box', label: 'Produtos', to: '/admin/produtos' },
  { icon: 'pi pi-tag', label: 'Categorias', to: '/admin/categorias' },
  { icon: 'pi pi-list-check', label: 'Solicitações', to: '/admin/solicitacoes' },
  { icon: 'pi pi-palette', label: 'Aparência', to: '/admin/loja' },
  { icon: 'pi pi-cog', label: 'Configurações', to: '/admin/configuracoes' },
]
</script>

<template>
  <aside class="w-60 bg-zinc-900 flex flex-col py-6 px-3 shrink-0">
    <div class="flex items-center gap-2 px-3 mb-8">
      <div class="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
        <i class="pi pi-shopping-bag text-white text-sm" />
      </div>
      <span class="font-bold text-white">Catálogo</span>
    </div>

    <nav class="flex flex-col gap-1 flex-1">
      <RouterLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all no-underline"
        :class="route.path === item.to
          ? 'bg-orange-500 text-white'
          : 'text-zinc-400 hover:bg-zinc-800 hover:text-white'"
      >
        <i :class="[item.icon, 'text-base']" />
        {{ item.label }}
      </RouterLink>
    </nav>

    <RouterLink
      to="/"
      class="flex items-center gap-2 px-3 py-2 text-xs text-zinc-500 hover:text-zinc-300 transition-colors no-underline mt-4"
    >
      <i class="pi pi-arrow-left text-xs" />
      Ver loja
    </RouterLink>
  </aside>
</template>
