<script setup lang="ts">
import { ref, watch, computed } from "vue"

const props = withDefaults(defineProps<{
    src?: string | null
    alt?: string
    aspect?: string
    icone?: string // classe primeicons, ex: "pi-shopping-bag"
}>(), {
    src: null,
    alt: "",
    aspect: "aspect-[4/5]",
    icone: "pi-image"
})

const erro = ref(false)
watch(() => props.src, () => { erro.value = false })

// Paleta alinhada à marca: variações de laranja + zinc neutro
const paleta = [
    { from: "#fed7aa", to: "#fb923c", fg: "#7c2d12" }, // laranja claro
    { from: "#fdba74", to: "#ea580c", fg: "#7c2d12" }, // laranja médio
    { from: "#e4e4e7", to: "#a1a1aa", fg: "#3f3f46" }, // zinc neutro
    { from: "#fecaca", to: "#f87171", fg: "#7f1d1d" }, // vermelho suave (contraste leve)
    { from: "#fde68a", to: "#fbbf24", fg: "#78350f" }, // âmbar
]

function hash(texto: string) {
    let h = 0
    for (let i = 0; i < texto.length; i++) {
        h = texto.charCodeAt(i) + ((h << 5) - h)
    }
    return Math.abs(h)
}

const cores = computed(() => paleta[hash(props.alt || "produto") % paleta.length])

const iniciais = computed(() => {
    const partes = (props.alt || "").trim().split(/\s+/).filter(Boolean)
    if (!partes.length) return "?"
    return partes.slice(0, 2).map(p => p[0].toUpperCase()).join("")
})
</script>

<template>
<div :class="[aspect, 'w-full overflow-hidden relative']">
    <img
        v-if="!erro && src"
        :src="src"
        :alt="alt"
        loading="lazy"
        class="w-full h-full object-cover object-center"
        @error="erro = true"
    >
    <div
        v-else
        class="w-full h-full flex flex-col items-center justify-center gap-1 select-none relative overflow-hidden"
        :style="{ background: `linear-gradient(135deg, ${cores.from}, ${cores.to})` }"
    >
        <!-- ícone sutil de fundo, grande e semi-transparente -->
        <i
            :class="['pi', icone, 'absolute text-6xl sm:text-7xl opacity-20']"
            :style="{ color: cores.fg }"
        />
        <!-- iniciais em destaque -->
        <span
            class="relative text-xl sm:text-2xl font-bold tracking-wide"
            :style="{ color: cores.fg }"
        >
            {{ iniciais }}
        </span>
    </div>
</div>
</template>