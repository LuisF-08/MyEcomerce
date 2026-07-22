<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useCarrinhoStore } from "@/stores/carrinho"

const carrinho = useCarrinhoStore()

const isMenuOpen = ref(false)
const isDark = ref(false)

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('my-app-dark')
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('my-app-dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <header class="sticky top-0 z-50 bg-white/95 dark:bg-zinc-950/95 backdrop-blur-sm border-b border-zinc-100 dark:border-zinc-800/60 shadow-sm dark:shadow-zinc-950/30 transition-all duration-300">
    <div class="max-w-7xl mx-auto px-4 md:px-6 h-16 flex items-center justify-between">
      
      <!-- Esquerda: Menu Hambúrguer (Apenas Mobile) e Logo -->
      <div class="flex items-center gap-2">
        <button 
          @click="isMenuOpen = !isMenuOpen"
          class="md:hidden w-10 h-10 flex items-center justify-center rounded-full text-zinc-600 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50 transition-colors"
          aria-label="Abrir menu"
        >
          <i :class="['pi', isMenuOpen ? 'pi-times' : 'pi-bars', 'text-xl']" />
        </button>

        <!-- Logo -->
        <RouterLink :to="{ name: 'home' }" @click="closeMenu" class="flex items-center gap-2 no-underline group">
          <div class="w-9 h-9 bg-orange-500 rounded-full flex items-center justify-center shadow-lg shadow-orange-500/20 transition-transform group-hover:scale-105">
            <i class="pi pi-shopping-bag text-white text-lg" />
          </div>
          <span class="font-bold text-zinc-950 dark:text-white text-xl tracking-tight">Catálogo<span class="text-orange-500">.</span></span>
        </RouterLink>
      </div>

      <!-- Centro: Navegação Principal (Desktop) -->
      <nav class="hidden md:flex items-center gap-1">
        <RouterLink 
          :to="{ name: 'home' }" 
          class="px-4 py-1.5 rounded-full text-sm font-medium no-underline transition-all duration-200"
          :class="[$route.name === 'home' ? 'bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400' : 'text-zinc-600 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/50']"
        >
          Início
        </RouterLink>
        <RouterLink 
          :to="{ name: 'produtos' }" 
          class="px-4 py-1.5 rounded-full text-sm font-medium no-underline transition-all duration-200"
          :class="[$route.name === 'produtos' ? 'bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400' : 'text-zinc-600 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/50']"
        >
          Produtos
        </RouterLink>
        <RouterLink 
          :to="{ name: 'sobre' }" 
          class="px-4 py-1.5 rounded-full text-sm font-medium no-underline transition-all duration-200"
          :class="[$route.name === 'sobre' ? 'bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400' : 'text-zinc-600 dark:text-zinc-300 hover:text-zinc-950 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/50']"
        >
          Sobre
        </RouterLink>
      </nav>

      <!-- Direita: Ações Globais -->
      <div class="flex items-center gap-2 md:gap-3">
        <!-- Modo Escuro -->
        <button 
          @click="toggleTheme"
          class="group relative w-10 h-10 flex items-center justify-center rounded-full border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 hover:bg-zinc-50 dark:hover:bg-zinc-800/80 transition-all duration-500 ease-in-out shadow-inner"
          aria-label="Alternar tema"
        >
          <div class="relative w-5 h-5 transition-transform duration-500" :class="{ 'rotate-[360deg]': isDark }">
            <i class="pi pi-sun text-lg absolute inset-0 text-amber-500 transition-all duration-500 transform" :class="isDark ? 'opacity-0 scale-0' : 'opacity-100 scale-100'" />
            <i class="pi pi-moon text-lg absolute inset-0 text-blue-400 transition-all duration-500 transform" :class="isDark ? 'opacity-100 scale-100' : 'opacity-0 scale-0'" />
          </div>
        </button>

        <!-- Carrinho -->
        <button
          class="relative w-10 h-10 flex items-center justify-center 
          rounded-full text-zinc-600 dark:text-zinc-300 hover:text-orange-600
           dark:hover:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-950/30 
           transition-all duration-200"
          @click="() => { carrinho.toggle(); closeMenu(); }">
          <i class="pi pi-shopping-cart text-xl" />
          <span class="absolute top-1 right-1 w-4 h-4 bg-orange-500
            text-white text-[10px] font-bold rounded-full flex items-center justify-center">
            {{ carrinho.quantidadeItens }}
          </span>
        </button>

        <div class="hidden sm:block w-px h-6 bg-zinc-200 dark:bg-zinc-800"></div>

        <!-- Admin (Desktop) -->
        <RouterLink
          :to="{ name: 'login' }"
          class="hidden sm:flex text-sm text-zinc-700 dark:text-zinc-200 font-semibold no-underline px-5 py-2.5 bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 rounded-full transition-all duration-200 items-center gap-2 shadow-sm"
        >
          <i class="pi pi-user text-sm text-zinc-500 dark:text-zinc-400" />
          Admin
        </RouterLink>
      </div>
    </div>

    <!-- ==========================================================================
      MENU RETRÁTIL MOBILE (Desliza para baixo de forma muito suave)
      ========================================================================== -->
    <div 
      class="md:hidden overflow-hidden transition-all duration-300 ease-in-out bg-white dark:bg-zinc-950 border-b border-zinc-100 dark:border-zinc-800/60"
      :class="[isMenuOpen ? 'max-h-64 opacity-100' : 'max-h-0 opacity-0']"
    >
      <div class="px-6 py-4 flex flex-col gap-2">
        <RouterLink 
          :to="{ name: 'home' }" 
          @click="closeMenu"
          class="w-full px-4 py-2.5 rounded-xl text-sm font-medium no-underline transition-all block"
          :class="[$route.name === 'home' ? 'bg-orange-50 dark:bg-orange-950/20 text-orange-600 dark:text-orange-400' : 'text-zinc-600 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-900']"
        >
          <i class="pi pi-home mr-2 text-xs" /> Início
        </RouterLink>
        
        <RouterLink 
          :to="{ name: 'produtos' }" 
          @click="closeMenu"
          class="w-full px-4 py-2.5 rounded-xl text-sm font-medium no-underline transition-all block"
          :class="[$route.name === 'produtos' ? 'bg-orange-50 dark:bg-orange-950/20 text-orange-600 dark:text-orange-400' : 'text-zinc-600 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-900']"
        >
          <i class="pi pi-box mr-2 text-xs" /> Produtos
        </RouterLink>

        <RouterLink 
          :to="{ name: 'sobre' }" 
          @click="closeMenu"
          class="w-full px-4 py-2.5 rounded-xl text-sm font-medium no-underline transition-all block"
          :class="[$route.name === 'sobre' ? 'bg-orange-50 dark:bg-orange-950/20 text-orange-600 dark:text-orange-400' : 'text-zinc-600 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-900']"
        >
          <i class="pi pi-info-circle mr-2 text-xs" /> Sobre
        </RouterLink>

        <!-- Link Admin exclusivo para Mobile (visível apenas em telas bem pequenas) -->
        <RouterLink
          :to="{ name: 'login' }"
          @click="closeMenu"
          class="sm:hidden w-full px-4 py-2.5 rounded-xl text-sm font-medium no-underline transition-all block text-zinc-600 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-900 border-t border-zinc-100 dark:border-zinc-900 mt-1 pt-3"
        >
          <i class="pi pi-user mr-2 text-xs" /> Admin
        </RouterLink>
      </div>
    </div>
  </header>
</template>