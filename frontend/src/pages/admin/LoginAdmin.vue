<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'primevue/usetoast'

import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'

const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const usuarioOuEmail = ref('')
const senha = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!usuarioOuEmail.value || !senha.value) {
    toast.add({
      severity: 'warn',
      summary: 'Atenção',
      detail: 'Preencha o usuário/e-mail e a senha.',
      life: 3000
    })
    return
  }

  loading.value = true
  try {
    // Adapta o payload para o contrato do Django Rest Framework (username / password)
    await auth.login({
      username: usuarioOuEmail.value.trim(),
      email: usuarioOuEmail.value.trim(),
      password: senha.value
    } as any)

    toast.add({
      severity: 'success',
      summary: 'Bem-vindo!',
      detail: 'Login realizado com sucesso.',
      life: 2500
    })

    // Redireciona para o nome correto da rota configurada no Vue Router
    router.push({ name: 'admin-dashboard' })
  } catch (error: any) {
    console.error('Erro ao efetuar login:', error)
    
    const mensagemErro = error.response?.data?.detail 
      || error.response?.data?.non_field_errors?.[0]
      || 'Usuário ou senha inválidos.'

    toast.add({
      severity: 'error',
      summary: 'Erro de Autenticação',
      detail: mensagemErro,
      life: 4000
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-zinc-50 flex items-center justify-center px-4">
    <div class="bg-white rounded-2xl shadow-lg border border-zinc-100 p-8 w-full max-w-sm">
      
      <!-- Cabeçalho do Card -->
      <div class="flex flex-col items-center mb-8">
        <div class="w-14 h-14 bg-orange-500 rounded-2xl flex items-center justify-center mb-4 shadow-md shadow-orange-500/20">
          <i class="pi pi-shopping-bag text-white text-2xl" />
        </div>
        <h1 class="text-xl font-extrabold text-zinc-900">Catálogo Digital</h1>
        <p class="text-xs font-medium text-zinc-500 mt-1 uppercase tracking-wider">Painel Administrativo</p>
      </div>

      <!-- Formuário -->
      <form class="space-y-4" @submit.prevent="handleLogin">
        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Usuário ou E-mail</label>
          <InputText
            v-model="usuarioOuEmail"
            type="text"
            placeholder="admin"
            class="w-full !rounded-xl"
            required
            autocomplete="username"
          />
        </div>

        <div>
          <label class="text-xs font-semibold text-zinc-600 mb-1 block">Senha</label>
          <Password
            v-model="senha"
            placeholder="••••••••"
            :feedback="false"
            toggle-mask
            class="w-full"
            input-class="w-full !rounded-xl"
            required
            autocomplete="current-password"
          />
        </div>

        <Button
          type="submit"
          label="Entrar no Painel"
          icon="pi pi-sign-in"
          class="w-full !bg-orange-500 !border-orange-500 hover:!bg-orange-600 !font-semibold !rounded-xl !py-3 mt-2 transition-all shadow-md shadow-orange-500/20"
          :loading="loading"
        />
      </form>

      <!-- Dica de Credenciais -->
      <div class="mt-6 pt-4 border-t border-zinc-100 text-center">
        <p class="text-xs text-zinc-400">
          Credenciais Superuser: <span class="font-mono font-medium text-zinc-600">admin / admin</span>
        </p>
      </div>

    </div>
  </div>
</template>