<script setup lang="ts">
import Navbar from '@/components/layout/Navbar.vue'
import PromoBanner from '@/components/layout/PromoBanner.vue'
import Footer from '@/components/layout/Footer.vue'
import CarrinhoDrawer from '@/components/cart/CarrinhoDrawer.vue'
import Toast from 'primevue/toast'
</script>

<template>
    <div>
        <Navbar />
        <PromoBanner />
        <CarrinhoDrawer />
        <Toast position="top-left" />
        <RouterView />
        <Footer />
    </div>
</template>