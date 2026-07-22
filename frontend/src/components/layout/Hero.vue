<script setup lang="ts">
import { ref} from 'vue'
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
  <!-- Hero -->
  <section class="bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 text-white py-20 px-4">
    <div class="max-w-4xl mx-auto text-center">
      <span class="inline-block bg-orange-500/20 text-orange-400 text-xs font-semibold px-3 py-1 rounded-full mb-4 uppercase tracking-widest">
        Catálogo Digital
      </span>
      <h1 class="text-4xl md:text-5xl font-extrabold leading-tight mb-4">
        Tudo que você precisa,<br />
        <span class="text-orange-400">direto no WhatsApp</span>
      </h1>
      <p class="text-zinc-400 text-lg mb-8 max-w-xl mx-auto">
        Explore nosso catálogo e faça seu pedido com facilidade. Entregamos onde você está.
      </p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center max-w-md mx-auto">
        <input
          v-model="busca"
          type="text"
          placeholder="Buscar produto..."
          class="flex-1 px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-zinc-500 focus:outline-none focus:border-orange-500 text-sm"
          @keyup.enter="buscar"
        />
        <button
          class="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-xl transition-colors text-sm"
          @click="buscar"
        >
          Buscar
        </button>
      </div>
    </div>
  </section>
</template>