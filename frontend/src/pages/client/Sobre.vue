<script setup lang="ts">
import { storeToRefs } from "pinia"
import { useLojaStore } from "@/stores/loja"
import Depoiments from "@/components/layout/Depoiments.vue";

const lojaStore = useLojaStore()
const { loja } = storeToRefs(lojaStore)

const formatarData = (data: string | undefined) => {
  if (!data) return 'Data não disponível';

  const date = new Date(data);

  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });
};
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-16">

    <!-- Header -->
    <div class="text-center mb-14">
      <span class="inline-flex items-center gap-2 bg-orange-50 dark:bg-orange-500/10 text-orange-600 dark:text-orange-400 text-xs font-semibold px-4 py-1.5 rounded-full mb-4 ring-1 ring-orange-100 dark:ring-orange-500/20">
        <i class="pi pi-heart-fill text-[10px]" />
        Nossa história
      </span>
      <h1 class="text-4xl font-extrabold text-zinc-900 dark:text-white mb-3 tracking-tight">Sobre nós</h1>
      <p class="text-zinc-500 dark:text-zinc-400 text-lg max-w-xl mx-auto">
        Criado em <span class="text-zinc-700 dark:text-zinc-200 font-medium">{{ formatarData(loja?.criado_em) }}</span>,
        conheça a nossa história e o que nos motiva.
      </p>
    </div>

    <!-- Story + Image -->
    <div class="grid md:grid-cols-2 gap-10 items-center mb-16">
      <div>
        <h2 class="text-xl font-bold text-zinc-900 dark:text-white mb-3 flex items-center gap-2">
          <span class="w-1.5 h-6 bg-orange-500 rounded-full" />
          Quem somos
        </h2>
        <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-sm mb-4">{{ loja?.descricao }}</p>
        <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-sm mb-4">
          Nascemos da vontade de facilitar o comércio local, conectando pequenos lojistas com seus clientes
          de forma simples e eficiente. Nosso catálogo digital permite que você explore produtos e faça pedidos
          diretamente pelo WhatsApp — sem complicações.
        </p>
        <p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-sm">
          Acreditamos que o comércio local tem um papel fundamental na economia e na vida das comunidades.
          Por isso, trabalhamos para oferecer as melhores ferramentas para quem vende com paixão.
        </p>
      </div>

      <div class="relative">
        <div class="absolute -inset-3 bg-gradient-to-br from-orange-200 via-orange-100 to-transparent dark:from-orange-500/20 dark:via-orange-500/5 dark:to-transparent rounded-3xl blur-xl opacity-70" />
        <div class="relative rounded-2xl overflow-hidden aspect-square shadow-lg ring-1 ring-black/5 dark:ring-white/10">
          <img
            src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=600&fit=crop&auto=format"
            alt="Nossa loja"
            class="w-full h-full object-cover"
          />
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-5 mb-16">
      <div
        v-for="s in [
          { value: '500+', label: 'Clientes atendidos', icon: 'pi-users' },
          { value: '8', label: 'Categorias', icon: 'pi-th-large' },
          { value: '50+', label: 'Produtos', icon: 'pi-box' },
          { value: '4.9★', label: 'Avaliação média', icon: 'pi-star-fill' },
        ]"
        :key="s.label"
        class="bg-gradient-to-b from-white to-orange-50/40 dark:from-zinc-900 dark:to-zinc-900/60 border border-orange-100 dark:border-zinc-800 rounded-2xl p-5 text-center hover:shadow-md dark:hover:border-orange-500/30 hover:-translate-y-0.5 transition-all duration-200"
      >
        <i :class="['pi', s.icon, 'text-orange-400 text-lg mb-2']" />
        <p class="text-2xl font-extrabold text-orange-500 dark:text-orange-400 mb-1">{{ s.value }}</p>
        <p class="text-xs text-zinc-500 dark:text-zinc-400 font-medium">{{ s.label }}</p>
      </div>
    </div>

    <Depoiments />

    <!-- Contact card -->
    <div class="relative overflow-hidden bg-gradient-to-br from-zinc-900 via-zinc-950 to-black dark:from-black dark:via-zinc-950 dark:to-black text-white rounded-2xl p-8 flex flex-col md:flex-row items-center justify-between gap-6 ring-1 ring-white/10">
      <div class="absolute -top-16 -right-16 w-56 h-56 bg-amber-500/10 rounded-full blur-3xl" />
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.04),transparent_60%)]" />

      <div class="relative">
        <h3 class="text-lg font-bold mb-1 flex items-center gap-2">
          Fale com a gente
          <span class="text-amber-400">✦</span>
        </h3>
        <p class="text-zinc-400 text-sm">Estamos disponíveis de segunda a sábado.</p>
        <p class="text-zinc-400 text-sm mt-2 flex items-center gap-2">
          <i class="pi pi-map-marker text-amber-400" />
          {{ loja?.numero }} ,{{ loja?.rua }} ,{{ loja?.bairro }} ,{{ loja?.cidade }} - {{ loja?.cep }}
        </p>
        <p class="text-zinc-400 text-sm mt-1 flex items-center gap-2">
          <i class="pi pi-clock text-amber-400" />
          Seg–Sex: 09h–18h | Sáb: 09h–14h
        </p>
      </div>

      <a
        href="https://wa.me/5511999999999"
        target="_blank"
        class="relative bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors flex items-center gap-2 no-underline shadow-lg shadow-green-500/20 ring-1 ring-white/10"
      >
        <i class="pi pi-whatsapp" />
        Falar no WhatsApp
      </a>
    </div>

  </div>
</template>