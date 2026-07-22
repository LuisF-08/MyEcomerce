<script setup lang="ts">
import { RouterView } from 'vue-router';
import Navbar from './components/layout/Navbar.vue';
import Footer from './components/layout/Footer.vue';
import CarrinhoDrawer from './components/cart/CarrinhoDrawer.vue';
import Toast from "primevue/toast"
</script>

<template>
  <div id="app">
    <Navbar />
    <CarrinhoDrawer />
    <Toast position="top-left" />
    <RouterView />
    <Footer />
  </div>
</template>