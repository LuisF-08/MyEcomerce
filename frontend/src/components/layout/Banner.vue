<script setup lang="ts">
import { ref } from 'vue'
import Galleria from 'primevue/galleria'

const banners = ref([
  {
    id: 1,
    title: 'Coleção de Inverno',
    subtitle: 'Até 50% de desconto nos novos produtos',
    image: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=80',
  },
  {
    id: 2,
    title: 'Frete Grátis',
    subtitle: 'Aproveite frete grátis em compras acima de R$ 199',
    image: 'https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=1200&q=80',
  },
  {
    id: 3,
    title: 'Novidades Semanais',
    subtitle: 'Confira os lançamentos que acabaram de chegar na loja',
    image: 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?auto=format&fit=crop&w=1200&q=80',
  },
  {
    id: 4,
    title: 'Cupons Especiais',
    subtitle: 'Use o cupom PRIMEIRACOMPRA e ganhe 10% OFF',
    image: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=1200&q=80',
  }
])

const responsiveOptions = ref([
  {
    breakpoint: '1024px',
    numVisible: 1
  }
])
</script>

<template>
  <div class="w-full max-w-7xl mx-auto px-4 md:px-6 py-6">
    <Galleria 
      :value="banners" 
      :responsiveOptions="responsiveOptions" 
      :numVisible="1" 
      :circular="true" 
      :autoPlay="true" 
      :transitionInterval="4000"
      :showThumbnails="false"
      :showIndicators="true"
      class="custom-banner"
    >
      <template #item="slotProps">
        <!-- 
          O banner interno agora controla 100% o arredondamento (rounded-3xl)
          e as sombras de forma limpa.
        -->
        <div class="relative w-full h-[300px] md:h-[450px] overflow-hidden rounded-3xl bg-zinc-100 dark:bg-zinc-900 shadow-sm border border-zinc-100 dark:border-zinc-800/50">
          
          <img 
            :src="slotProps.item.image" 
            :alt="slotProps.item.title" 
            class="w-full h-full object-cover" 
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent flex flex-col justify-end p-6 md:p-12">
            <span class="text-xs md:text-sm font-semibold tracking-wider text-orange-400 uppercase mb-2">
              Destaque
            </span>
            <h2 class="text-2xl md:text-5xl font-extrabold text-white mb-2 md:mb-4 tracking-tight">
              {{ slotProps.item.title }}
            </h2>
            <p class="text-sm md:text-lg text-zinc-200 max-w-xl font-medium">
              {{ slotProps.item.subtitle }}
            </p>
          </div>

        </div>
      </template>
    </Galleria>
  </div>
</template>

<style scoped>
/* ==========================================================================
   RESETS DO PRIMEVUE GALLERIA (Remove a caixa quadrada e o fundo cinza)
   ========================================================================== */

/* Remove a borda e o fundo cinza da estrutura externa principal */
:deep(.p-galleria) {
  border: none !important;
  background: transparent !important;
}

/* Remove fundos e bordas do contêiner interno de itens */
:deep(.p-galleria-content),
:deep(.p-galleria-item-wrapper),
:deep(.p-galleria-item-container) {
  background: transparent !important;
  border: none !important;
}

/* ==========================================================================
   ESTILIZAÇÃO DOS INDICADORES (Bolinhas embaixo do banner)
   ========================================================================== */

/* Remove qualquer fundo ou borda cinza que o PrimeVue coloca atrás das bolinhas */
:deep(.p-galleria-indicators) {
  background: transparent !important;
  border: none !important;
  padding: 1rem 0 0 0 !important;
  gap: 0.5rem;
  justify-content: center;
}

/* Reseta o botão invisível que fica em volta de cada bolinha */
:deep(.p-galleria-indicator) {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Estilo padrão da bolinha (Inativa) */
:deep(.p-galleria-indicator button) {
  width: 10px !important;
  height: 10px !important;
  border-radius: 9999px !important;
  background-color: #e4e4e7 !important; /* zinc-200 */
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Estilo da bolinha ATIVA (Agora vai mudar perfeitamente para Laranja) */
:deep(.p-galleria-indicator.p-galleria-indicator-active button) {
  width: 28px !important; /* Estica suavemente estilo pílula */
  background-color: #f97316 !important; /* Cor Laranja Primária */
}

/* Ajustes finos para o Dark Mode */
:global(.my-app-dark) :deep(.p-galleria-indicator button) {
  background-color: #3f3f46 !important; /* zinc-700 */
}

:global(.my-app-dark) :deep(.p-galleria-indicator.p-galleria-indicator-active button) {
  background-color: #414141 !important; /* Mantém o laranja vivo no dark */
}
</style>