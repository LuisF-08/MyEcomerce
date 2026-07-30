<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const busca = ref('')

const buscar = () => {
  if (busca.value.trim()) {
    router.push({ name: 'categoria', params: { slug: 'todos' }, query: { q: busca.value } })
  }
}
</script>

<template>
  <!-- Hero Original -->
  <section class="relative overflow-hidden bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 text-white py-20 px-4">
    <!-- Orbes decorativos de luz (puramente visuais) -->
    <div class="pointer-events-none absolute -top-24 -left-24 w-72 h-72 bg-orange-500/20 rounded-full blur-3xl"></div>
    <div class="pointer-events-none absolute -bottom-24 -right-24 w-80 h-80 bg-orange-400/10 rounded-full blur-3xl"></div>

    <div class="relative max-w-4xl mx-auto text-center">
      <span class="inline-block bg-orange-500/20 backdrop-blur-sm border border-orange-400/20 text-orange-400 text-xs font-semibold px-3 py-1 rounded-full mb-4 uppercase tracking-widest shadow-sm">
        Catálogo Digital
      </span>

      <h1 class="text-4xl md:text-5xl font-extrabold leading-tight mb-4 drop-shadow-sm">
        Tudo que você precisa,<br />
        <span class="text-orange-400">direto no WhatsApp</span>
      </h1>

      <p class="text-zinc-400 text-lg mb-8 max-w-xl mx-auto">
        Explore nosso catálogo e faça seu pedido com facilidade. Entregamos onde você está.
      </p>

      <!-- Cartão de vidro envolvendo a busca -->
      <div class="max-w-md mx-auto p-2 rounded-2xl bg-white/5 backdrop-blur-md border border-white/10 shadow-[0_8px_32px_rgba(0,0,0,0.3)] ring-1 ring-white/5">
        <div class="flex flex-col sm:flex-row gap-3">
          <input
            v-model="busca"
            type="text"
            placeholder="Buscar produto..."
            class="flex-1 px-4 py-3 rounded-xl bg-zinc-900/60 backdrop-blur-sm border border-zinc-700/50 text-white placeholder-zinc-500 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-500/30 text-sm transition-all"
            @keyup.enter="buscar"
          />
          <button
            class="px-6 py-3 bg-gradient-to-b from-orange-500 to-orange-600 hover:from-orange-400 hover:to-orange-600 text-white font-semibold rounded-xl transition-all text-sm shadow-lg shadow-orange-500/20 hover:shadow-orange-500/30 active:scale-95"
            @click="buscar"
          >
            Buscar
          </button>
        </div>
      </div>
    </div>
  </section>
</template>