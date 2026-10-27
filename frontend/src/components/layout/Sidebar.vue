<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import BrandLogo from '@/components/common/BrandLogo.vue'

const props = defineProps<{ mobileOpen?: boolean }>()
const emit = defineEmits<{ close: [] }>()

const route = useRoute()

const menuItems = [
  { label: 'Dashboard', icon: 'pi pi-home', routeName: 'admin-dashboard' },
  { label: 'Produtos', icon: 'pi pi-box', routeName: 'admin-produtos' },
  { label: 'Categorias', icon: 'pi pi-tags', routeName: 'admin-categorias' },
  { label: 'Solicitações', icon: 'pi pi-inbox', routeName: 'admin-solicitacoes' },
  { label: 'Aparência', icon: 'pi pi-palette', routeName: 'admin-loja' },
  { label: 'Configurações', icon: 'pi pi-cog', routeName: 'admin-configuracoes' }
]

const pinned = ref(true)
const hovering = ref(false)

const isExpanded = computed(() => pinned.value || hovering.value)
const isFloatingOverlay = computed(() => !pinned.value && hovering.value)

// Larguras só valem a partir de md (desktop). No mobile é sempre 260px na gaveta.
const slotWidthClass = computed(() => (pinned.value ? 'md:w-[260px]' : 'md:w-[76px]'))
const asideWidthClass = computed(() => (isExpanded.value ? 'md:w-[260px]' : 'md:w-[76px]'))

function togglePin() {
  pinned.value = !pinned.value
  hovering.value = false
}
function handleMouseEnter() {
  if (!pinned.value) hovering.value = true
}
function handleMouseLeave() {
  hovering.value = false
}

// Fecha a gaveta ao navegar
watch(() => route.fullPath, () => emit('close'))

const isDark = ref(false)

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('my-app-dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('my-app-dark')
})
</script>

<template>
  <!-- Fundo escurecido (apenas mobile) -->
  <div
    v-if="props.mobileOpen"
    class="fixed inset-0 z-40 bg-black/50 md:hidden"
    @click="emit('close')"
  />

  <!-- Mobile: gaveta fixa que desliza. Desktop: coluna sticky no layout. -->
  <div
    class="fixed inset-y-0 left-0 z-50 w-[260px] transition-transform duration-300 ease-in-out
           md:sticky md:inset-y-auto md:top-0 md:h-dvh md:shrink-0 md:translate-x-0
           md:transition-[width]"
    :class="[props.mobileOpen ? 'translate-x-0' : '-translate-x-full', slotWidthClass]"
  >
    <aside
      class="absolute inset-y-0 left-0 z-40 flex flex-col gap-2 overflow-hidden w-[260px]
             bg-white dark:bg-zinc-950 md:bg-white/95 md:dark:bg-zinc-950/95 backdrop-blur-sm
             border-r border-zinc-100 dark:border-zinc-800/60
             transition-[width,box-shadow] duration-300 ease-in-out"
      :class="[
        asideWidthClass,
        isFloatingOverlay
          ? 'shadow-2xl shadow-zinc-950/20 dark:shadow-black/50 rounded-r-2xl border'
          : 'shadow-sm'
      ]"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
    >
    <!-- Header -->
    <div class="flex items-center justify-between px-3 pt-4 pb-3 min-h-[56px]">
      <div class="flex items-center overflow-hidden">
        <BrandLogo size="md" :show-name="isExpanded" />
      </div>
    
      <!-- Fixar/recolher: só desktop -->
      <button
        v-show="isExpanded"
        @click="togglePin"
        class="hidden md:flex w-8 h-8 shrink-0 items-center justify-center rounded-full text-zinc-500 dark:text-zinc-400 transition-colors duration-200 hover:bg-orange-50 dark:hover:bg-orange-950/30 hover:text-orange-500"
        :aria-label="pinned ? 'Recolher menu' : 'Fixar menu'"
      >
        <i :class="['pi', pinned ? 'pi-angle-left' : 'pi-angle-right']" />
      </button>
    
      <!-- Fechar: só mobile -->
      <button
        class="md:hidden w-8 h-8 shrink-0 flex items-center justify-center rounded-full text-zinc-500 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800/50"
        aria-label="Fechar menu"
        @click="emit('close')"
      >
        <i class="pi pi-times" />
      </button>
    </div>

      <!-- Navegação -->
      <nav class="flex-1 overflow-y-auto overflow-x-hidden px-2">
        <span
          v-show="isExpanded"
          class="block px-2.5 pt-1 pb-2 text-[11px] font-bold tracking-wider uppercase text-zinc-400 dark:text-zinc-500 whitespace-nowrap"
        >
          Catálogo
        </span>

        <ul class="flex flex-col gap-0.5 list-none m-0 p-0">
          <li v-for="item in menuItems" :key="item.routeName">
            <RouterLink
              :to="{ name: item.routeName }"
              :title="!isExpanded ? item.label : undefined"
              class="group relative flex items-center gap-3 h-11 px-2.5 rounded-xl no-underline whitespace-nowrap
                     text-zinc-600 dark:text-zinc-300
                     transition-colors duration-200
                     hover:bg-orange-50 dark:hover:bg-orange-950/20
                     hover:text-orange-500 dark:hover:text-orange-400"
              :class="[
                isExpanded ? '' : 'justify-center px-0',
                route.name === item.routeName ? 'bg-zinc-100 dark:bg-zinc-800/60 font-semibold' : ''
              ]"
            >
              <span
                v-if="route.name === item.routeName"
                class="absolute left-0 top-1/2 -translate-y-1/2 h-5 w-[3px] rounded-full bg-orange-500"
              />
              <i
                :class="[item.icon, 'text-[1.05rem] w-5 text-center shrink-0 transition-transform duration-200 group-hover:scale-110']"
              />
              <span v-show="isExpanded" class="text-sm">{{ item.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- Rodapé -->
      <div class="flex flex-col gap-2 px-2 pb-3 pt-2 border-t border-zinc-100 dark:border-zinc-800/60">
        <div class="flex items-center gap-3 h-11 px-2.5" :class="isExpanded ? '' : 'justify-center px-0'">
          <button
            @click="toggleTheme"
            class="group relative w-9 h-9 shrink-0 flex items-center justify-center rounded-full border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 hover:bg-zinc-50 dark:hover:bg-zinc-800/80 transition-all duration-500 ease-in-out shadow-inner"
            aria-label="Alternar tema"
          >
            <div class="relative w-5 h-5 transition-transform duration-500" :class="{ 'rotate-[360deg]': isDark }">
              <i
                class="pi pi-sun text-lg absolute inset-0 text-amber-500 transition-all duration-500 transform"
                :class="isDark ? 'opacity-0 scale-0' : 'opacity-100 scale-100'"
              />
              <i
                class="pi pi-moon text-lg absolute inset-0 text-blue-400 transition-all duration-500 transform"
                :class="isDark ? 'opacity-100 scale-100' : 'opacity-0 scale-0'"
              />
            </div>
          </button>
          <span v-show="isExpanded" class="text-sm text-zinc-600 dark:text-zinc-300 whitespace-nowrap">
            {{ isDark ? 'Modo escuro' : 'Modo claro' }}
          </span>
        </div>

        <RouterLink
          :to="{ name: 'home' }"
          :title="!isExpanded ? 'Ver loja' : undefined"
          class="group flex items-center gap-3 h-11 px-2.5 rounded-xl no-underline whitespace-nowrap
                 text-zinc-700 dark:text-zinc-200 font-semibold
                 bg-zinc-100 dark:bg-zinc-800
                 transition-colors duration-200
                 hover:bg-orange-50 dark:hover:bg-orange-950/20 hover:text-orange-500 dark:hover:text-orange-400"
          :class="isExpanded ? '' : 'justify-center px-0'"
        >
          <i class="pi pi-shop text-[1.05rem] w-5 text-center shrink-0 transition-transform duration-200 group-hover:scale-110" />
          <span v-show="isExpanded" class="text-sm">Ver loja</span>
        </RouterLink>
      </div>
    </aside>
  </div>
</template>