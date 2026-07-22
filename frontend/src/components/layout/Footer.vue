<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { storeToRefs } from "pinia"

import { useLojaStore } from "@/stores/loja"

const lojaStore = useLojaStore()

const { loja } = storeToRefs(lojaStore)
</script>

<template>
  <footer class="bg-zinc-900 text-zinc-400">
    <div class="max-w-6xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
      <div>
        <div class="flex items-center gap-2 mb-3">
          <div class="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
            <i class="pi pi-shopping-bag text-white text-sm" />
          </div>
          <span class="font-bold text-white text-lg">{{ loja?.nome }}</span>
        </div>
        <p class="text-sm leading-relaxed">Sua loja digital para vender pelo WhatsApp com facilidade.</p>
      </div>
      <div>
        <h4 class="font-semibold text-white mb-3 text-sm">Navegação</h4>
        <ul class="space-y-2 text-sm">
          <li><RouterLink to="/" class="hover:text-white transition-colors no-underline text-zinc-400">Início</RouterLink></li>
          <li><RouterLink to="/categoria/todos" class="hover:text-white transition-colors no-underline text-zinc-400">Produtos</RouterLink></li>
          <li><RouterLink to="/sobre" class="hover:text-white transition-colors no-underline text-zinc-400">Sobre nós</RouterLink></li>
          <li><RouterLink to="/carrinho" class="hover:text-white transition-colors no-underline text-zinc-400">Carrinho</RouterLink></li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold text-white mb-3 text-sm">Contato</h4>
        <ul class="space-y-2 text-sm">
          <li class="flex items-center gap-2"><i class="pi pi-whatsapp text-green-400" /> {{ loja?.whatsapp }}</li>
          <li class="flex items-center gap-2"><i class="pi pi-map-marker text-orange-400" /> {{ loja?.cidade }} - {{ loja?.rua}} - {{ loja?.numero }} - {{ loja?.referencia }}</li>
          <li class="flex items-center gap-2"><i class="pi pi-clock text-blue-400" /> {{ loja?.dias_funcionamento }} | {{ loja?.horario_funcionamento }} - {{loja?.horario_funcionamento}}</li>
          <li class="flex items-center gap-2"><i class="pi pi-address-book text-blue-600" /> {{ loja?.cnpj }}</li>
        </ul>
      </div>
      <div>
        <h4 class="font-semibold text-white mb-3 text-sm">Social</h4>
        <div class="flex gap-3">
          <a href="#" class="w-9 h-9 rounded-xl bg-zinc-800 flex items-center justify-center hover:bg-orange-500 transition-colors">
            <i class="pi pi-instagram text-sm text-white" />
          </a>
          <a href="#" class="w-9 h-9 rounded-xl bg-zinc-800 flex items-center justify-center hover:bg-blue-700 transition-colors">
            <i class="pi pi-facebook text-sm text-white" />
          </a>
          <a href="#" class="w-9 h-9 rounded-xl bg-zinc-800 flex items-center justify-center hover:bg-green-500 transition-colors">
            <i class="pi pi-whatsapp text-sm text-white" />
          </a>
          <a href="#" class="w-9 h-9 rounded-xl bg-zinc-800 flex items-center justify-center hover:bg-red-500 transition-colors">
            <i class="pi pi-inbox text-sm text-white" />
          </a>
        </div>
      </div>
    </div>
    <div class="border-t border-zinc-800 text-center py-4 text-xs text-zinc-600">
      © {{ new Date().getFullYear() }} CatálogoDigital. Todos os direitos reservados.
    </div>
  </footer>
</template>
