<script setup lang="ts">
</script>

<template>
  <!-- Banner Principal com a Imagem hero_principal.png (Ocupa todo o espaço e é totalmente responsivo) -->
  <div class="relative w-full overflow-hidden bg-zinc-900 shadow-2xl">
    <!-- Glow decorativo de fundo -->
    <div class="pointer-events-none absolute -inset-1 bg-gradient-to-r from-orange-500/10 via-transparent to-orange-500/10 blur-2xl"></div>

    <!-- Moldura de vidro -->
    <div class="relative border border-white/10 ring-1 ring-white/5 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)]">
      <img
        src="/banner_hero_primeiro2.png"
        alt="Banner Principal E-commerce"
        class="w-full h-auto block object-cover object-center max-h-[600px] transition-all duration-300"
      />

      <!-- Reflexo sutil no topo (efeito vidro) -->
      <div class="pointer-events-none absolute inset-x-0 top-0 h-1/3 bg-gradient-to-b from-white/10 to-transparent"></div>

      <!-- Vinheta sutil nas bordas para profundidade -->
      <div class="pointer-events-none absolute inset-0 shadow-[inset_0_-60px_60px_-40px_rgba(0,0,0,0.4)]"></div>
    </div>
  </div>
</template>

<style scoped>
/* Garante ajuste fluido em telas retina e mobile */
img {
  image-rendering: -webkit-optimize-contrast;
}
</style>