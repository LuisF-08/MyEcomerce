<script setup lang="ts">
</script>

<template>
  <section class="section-header">
    <span class="eyebrow">Navegue por</span>
    <h1 class="title-heading">Categorias</h1>
    <span class="accent-line" />
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