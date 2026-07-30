<script setup lang="ts">
const promoItems = [
  'OFERTAS IMPERDÍVEIS DA SEMANA',
  'ATÉ 50% OFF EM PRODUTOS SELECIONADOS',
  'FRETE GRÁTIS EM COMPRAS ACIMA DE R$ 199',
  '10% DE DESCONTO NO PIX COM CUPOM PRIMEIRACOMPRA',
  'PARCELAMENTO EM ATÉ 12X SEM JUROS NO CARTÃO',
  'FAÇA SEU PEDIDO RÁPIDO DIRETO NO WHATSAPP'
]
</script>

<template>
  <div class="w-full bg-amber-400 dark:bg-amber-500 text-amber-950 
  font-extrabold py-1 sm:py-1.5 overflow-hidden border-b
   border-amber-500/40 shadow-sm relative select-none">
    <div class="marquee-track flex whitespace-nowrap items-center
     hover:[animation-play-state:paused]">
      <!-- Bloco 1 -->
      <div class="flex items-center gap-6 shrink-0 pr-6">
        <template v-for="(item, index) in promoItems" :key="'a-' + index">
          <span class="flex items-center gap-2 text-xs sm:text-sm uppercase tracking-wider font-extrabold">
            <span class="text-sm sm:text-base animate-pulse">🔥</span>
            <span>{{ item }}</span>
          </span>
          <span class="text-amber-800/50 font-black">•</span>
        </template>
      </div>

      <!-- Bloco 2 (duplicado para loop infinito contínuo) -->
      <div class="flex items-center gap-6 shrink-0 pr-6">
        <template v-for="(item, index) in promoItems" :key="'b-' + index">
          <span class="flex items-center gap-2 text-xs sm:text-sm uppercase tracking-wider font-extrabold">
            <span class="text-sm sm:text-base animate-pulse">🔥</span>
            <span>{{ item }}</span>
          </span>
          <span class="text-amber-800/50 font-black">•</span>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.marquee-track {
  display: flex;
  width: max-content;
  animation: marquee 22s linear infinite;
}

@keyframes marquee {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-50%);
  }
}
</style>
