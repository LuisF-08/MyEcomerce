<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Categoria } from '@/types/categoria'

const props = defineProps<{ categoria: Categoria }>()
const router = useRouter()

function navegarParaCategoria() {
  router.push({
    path: '/produtos',
    query: { categoria: props.categoria.id }
  })
}
</script>

<template>
  <div
    v-ripple
    role="button"
    tabindex="0"
    class="ticket-card group"
    @click="navegarParaCategoria"
    @keydown.enter="navegarParaCategoria"
    @keydown.space.prevent="navegarParaCategoria"
  >
    <!-- Selo / ícone -->
    <div class="badge">
      <img
        v-if="categoria.imagem"
        :src="categoria.imagem"
        :alt="categoria.nome"
        loading="lazy"
      />
      <i v-else class="pi pi-tag" />
    </div>

    <!-- Divisória picotada com "furos" de ticket -->
    <div class="stub-divider">
      <span class="notch notch-top" />
      <span class="notch notch-bottom" />
    </div>

    <!-- Conteúdo -->
    <div class="content">
      <span class="title">{{ categoria.nome }}</span>
      <span v-if="categoria.descricao" class="subtitle">{{ categoria.descricao }}</span>
    </div>

    <i class="pi pi-arrow-right arrow" />
  </div>
</template>

<style scoped>
.ticket-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0;
  padding: 0.9rem 1.1rem 0.9rem 0.9rem;
  border-radius: 1.25rem;
  cursor: pointer;
  user-select: none;
  overflow: hidden;
  isolation: isolate;

  background: var(--p-content-background);
  border: 1px solid var(--p-content-border-color);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: transform 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease;
}

.ticket-card:hover {
  transform: translateY(-3px);
  border-color: color-mix(in srgb, var(--p-primary-color) 45%, var(--p-content-border-color));
  box-shadow:
    0 10px 24px -12px color-mix(in srgb, var(--p-primary-color) 35%, transparent),
    0 1px 2px rgba(0, 0, 0, 0.04);
}

.ticket-card:focus-visible {
  outline: 2px solid var(--p-primary-color);
  outline-offset: 2px;
}

/* Selo circular do ícone */
.badge {
  flex-shrink: 0;
  width: 3.1rem;
  height: 3.1rem;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: color-mix(in srgb, var(--p-primary-color) 12%, var(--p-content-background));
  border: 1.5px solid color-mix(in srgb, var(--p-primary-color) 25%, transparent);
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.3s ease;
}

.ticket-card:hover .badge {
  transform: scale(1.08) rotate(-4deg);
  background: color-mix(in srgb, var(--p-primary-color) 20%, var(--p-content-background));
}

.badge img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.badge .pi {
  font-size: 1.15rem;
  color: var(--p-primary-color);
}

/* Divisória estilo canhoto de ticket */
.stub-divider {
  position: relative;
  align-self: stretch;
  width: 1.5rem;
  margin: 0 0.35rem;
  display: flex;
  justify-content: center;
}

.stub-divider::before {
  content: '';
  width: 0;
  border-left: 1.5px dashed var(--p-content-border-color);
  transition: border-color 0.28s ease;
}

.ticket-card:hover .stub-divider::before {
  border-color: color-mix(in srgb, var(--p-primary-color) 40%, var(--p-content-border-color));
}

.notch {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 0.85rem;
  height: 0.85rem;
  border-radius: 999px;
  background: var(--p-surface-ground, var(--p-surface-100));
}

.notch-top {
  top: -1.35rem;
}

.notch-bottom {
  bottom: -1.35rem;
}

/* Texto */
.content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  padding-left: 0.15rem;
}

.title {
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  /* light mode mais escuro; dark mode segue token do PrimeVue */
  color: #1f1f23;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.28s ease;
}

:global(.dark) .title,
:global(html.dark) .title {
  color: var(--p-text-color);
}

.ticket-card:hover .title {
  color: var(--p-primary-color) !important;
}

.subtitle {
  margin-top: 0.15rem;
  font-size: 0.75rem;
  color: #52525b; /* zinc-600, mais escuro no light */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

:global(.dark) .subtitle,
:global(html.dark) .subtitle {
  color: var(--p-text-muted-color);
}

/* Seta */
.arrow {
  flex-shrink: 0;
  margin-left: 0.5rem;
  font-size: 0.7rem;
  color: #71717a;
  opacity: 0;
  transform: translateX(-6px);
  transition: all 0.28s ease;
}

:global(.dark) .arrow,
:global(html.dark) .arrow {
  color: var(--p-text-muted-color);
}

.ticket-card:hover .arrow {
  opacity: 1;
  transform: translateX(0);
  color: var(--p-primary-color) !important;
}

@media (max-width: 420px) {
  .ticket-card {
    padding: 0.7rem 0.85rem 0.7rem 0.7rem;
    border-radius: 1rem;
  }
  .badge {
    width: 2.6rem;
    height: 2.6rem;
  }
  .stub-divider {
    width: 1rem;
    margin: 0 0.2rem;
  }
  .title {
    font-size: 0.85rem;
  }
  .subtitle {
    font-size: 0.7rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ticket-card,
  .badge,
  .title,
  .arrow,
  .stub-divider::before {
    transition: none !important;
  }
}
</style>