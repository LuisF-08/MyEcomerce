import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import 'primeicons/primeicons.css'
import './assets/main.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth' // Import necessário para recuperar a sessão

// 1. Detecção Automática do Tema
document.documentElement.classList.add('no-transition')

const savedTheme = localStorage.getItem('theme')
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
  document.documentElement.classList.add('my-app-dark')
} else {
  document.documentElement.classList.remove('my-app-dark')
}

requestAnimationFrame(() => {
  requestAnimationFrame(() => {
    document.documentElement.classList.remove('no-transition')
  })
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ToastService);

app.use(PrimeVue, {
  ripple: true,
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.my-app-dark',
      cssLayer: false,
    },
  },
})

app.use(ToastService)
app.use(ConfirmationService)

const authStore = useAuthStore()
if (typeof authStore.carregarUsuario === 'function') {
  authStore.carregarUsuario()
}

app.mount('#app')