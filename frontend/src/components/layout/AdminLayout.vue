<script setup lang="ts">
import { RouterView } from "vue-router"
import Toast from "primevue/toast"
import Sidebar from "@/components/layout/Sidebar.vue"
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <Sidebar />
    <main class="flex-1 overflow-y-auto">
      <Toast />
      <RouterView />
    </main>
  </div>
</template>