<script setup lang="ts">
import { ref } from 'vue'

interface Depoimento {
  nome: string
  cidade: string
  nota: number
  comentario: string
  avatar: string
}

const depoimentos: Depoimento[] = [
  {
    nome: 'Mariana Souza',
    cidade: 'Guanambi, BA',
    nota: 5,
    comentario: 'Atendimento excelente e entrega super rápida. Já é a terceira vez que compro e sempre supera as expectativas!',
    avatar: 'https://i.pravatar.cc/100?img=47',
  },
  {
    nome: 'Carlos Eduardo',
    cidade: 'Vitória da Conquista, BA',
    nota: 5,
    comentario: 'Produtos de ótima qualidade e o pedido pelo WhatsApp foi muito prático. Recomendo demais!',
    avatar: 'https://i.pravatar.cc/100?img=12',
  },
  {
    nome: 'Fernanda Lima',
    cidade: 'Salvador, BA',
    nota: 4,
    comentario: 'Gostei muito da variedade de produtos. Só demorou um pouco mais que o esperado, mas valeu a pena.',
    avatar: 'https://i.pravatar.cc/100?img=32',
  },
  {
    nome: 'João Pedro',
    cidade: 'Barreiras, BA',
    nota: 5,
    comentario: 'Loja de confiança, já indiquei para toda minha família. Atendimento nota 10!',
    avatar: 'https://i.pravatar.cc/100?img=68',
  },
  {
    nome: 'Beatriz Alves',
    cidade: 'Ilhéus, BA',
    nota: 5,
    comentario: 'Superou minhas expectativas. Embalagem caprichada e produto exatamente como no catálogo.',
    avatar: 'https://i.pravatar.cc/100?img=25',
  },
  {
    nome: 'Lucas Monteiro',
    cidade: 'Brumado, BA',
    nota: 4,
    comentario: 'Ótimo preço e bem embalado o produto, chegou antes do prazo e assitêcia incrível!.',
    avatar: 'https://i.pravatar.cc/100?img=54',
  },
]

const trackRef = ref<HTMLElement | null>(null)

const scroll = (direction: 'left' | 'right') => {
  if (!trackRef.value) return
  const amount = trackRef.value.clientWidth * 0.85
  trackRef.value.scrollBy({
    left: direction === 'left' ? -amount : amount,
    behavior: 'smooth',
  })
}
</script>

<template>
  <section class="w-full max-w-full overflow-x-hidden mx-auto px-4 py-16">

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
      <div>
        <span class="inline-flex items-center gap-2 bg-orange-50 dark:bg-orange-500/10 text-orange-600 dark:text-orange-400 text-xs font-semibold px-4 py-1.5 rounded-full mb-3 ring-1 ring-orange-100 dark:ring-orange-500/20">
          <i class="pi pi-comments text-[10px]" />
          Depoimentos
        </span>
        <h2 class="text-2xl sm:text-3xl font-extrabold text-zinc-900 dark:text-white tracking-tight">
          O que dizem sobre nós
        </h2>
      </div>

      <!-- Setas -->
      <div class="hidden sm:flex gap-2 shrink-0">
        <button
          @click="scroll('left')"
          class="w-10 h-10 flex items-center justify-center rounded-full border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-orange-50 dark:hover:bg-zinc-800 hover:border-orange-300 dark:hover:border-orange-500/40 transition-colors"
        >
          <i class="pi pi-chevron-left text-sm" />
        </button>
        <button
          @click="scroll('right')"
          class="w-10 h-10 flex items-center justify-center rounded-full border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 hover:bg-orange-50 dark:hover:bg-zinc-800 hover:border-orange-300 dark:hover:border-orange-500/40 transition-colors"
        >
          <i class="pi pi-chevron-right text-sm" />
        </button>
      </div>
    </div>

    <!-- Carrossel -->
    <div
      ref="trackRef"
      class="flex gap-4 sm:gap-5 overflow-x-auto overscroll-x-contain snap-x snap-mandatory scroll-smooth pb-4 -mx-4 px-4
             [-webkit-overflow-scrolling:touch]
             [&::-webkit-scrollbar]:h-1.5
             [&::-webkit-scrollbar-track]:bg-transparent
             [&::-webkit-scrollbar-thumb]:bg-orange-200
             dark:[&::-webkit-scrollbar-thumb]:bg-zinc-700
             [&::-webkit-scrollbar-thumb]:rounded-full"
    >
      <div
        v-for="d in depoimentos"
        :key="d.nome"
        class="snap-start shrink-0 w-[78vw] xs:w-[260px] sm:w-[300px] max-w-[320px] bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl p-5 sm:p-6 flex flex-col hover:shadow-md dark:hover:border-orange-500/30 transition-all duration-200"
      >
        <!-- Estrelas -->
        <div class="flex gap-0.5 mb-3">
          <i
            v-for="n in 5"
            :key="n"
            :class="[
              'pi text-sm',
              n <= d.nota ? 'pi-star-fill text-amber-400' : 'pi-star text-zinc-300 dark:text-zinc-700'
            ]"
          />
        </div>

        <!-- Comentário -->
        <p class="text-zinc-600 dark:text-zinc-400 text-sm leading-relaxed mb-6 flex-1">
          "{{ d.comentario }}"
        </p>

        <!-- Autor -->
        <div class="flex items-center gap-3 pt-4 border-t border-zinc-100 dark:border-zinc-800">
          <img
            :src="d.avatar"
            :alt="d.nome"
            class="w-10 h-10 rounded-full object-cover ring-2 ring-orange-100 dark:ring-orange-500/20 shrink-0"
          />
          <div class="min-w-0">
            <p class="text-sm font-semibold text-zinc-900 dark:text-white truncate">{{ d.nome }}</p>
            <p class="text-xs text-zinc-400 dark:text-zinc-500 truncate">{{ d.cidade }}</p>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>