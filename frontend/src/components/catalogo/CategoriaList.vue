<script setup lang="ts">
</script>

<template>
  <section class="flex flex-col items-center text-center mb-6 sm:mb-7 px-4">
    <span class="text-[11px] font-bold tracking-[0.14em] uppercase text-orange-600 dark:text-orange-400 mb-1">
      Navegue por
    </span>
    <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">
      Categorias
    </h2>
    <span class="mt-2.5 h-[3px] w-10 rounded-full bg-orange-500" />
  </section>
</template>

<style scoped>
.section-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 1.75rem;
}

.eyebrow {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--p-primary-color);
  margin-bottom: 0.25rem;
}

.title-heading {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #1f1f23;
}

:global(.dark) .title-heading,
:global(html.dark) .title-heading {
  color: #f4f4f5;
}

.accent-line {
  width: 2.5rem;
  height: 3px;
  border-radius: 999px;
  margin-top: 0.65rem;
  background: var(--p-primary-color);
}

@media (max-width: 420px) {
  .title-heading {
    font-size: 1.4rem;
  }
}
</style>