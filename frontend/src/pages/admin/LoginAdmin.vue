<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth.ts"

import axios from "axios"

const router = useRouter()

const auth = useAuthStore()

const email = ref("")
const senha = ref("")

const entrar = async () => {

    try {

        await auth.login(
            email.value,
            senha.value
        )

        router.push("/dashboard")

    } catch (error) {

        if (axios.isAxiosError(error)) {

            alert(
                error.response?.data?.detail ??
                "Usuário ou senha inválidos."
            )

        } else {

            alert("Erro inesperado.")

        }

    }

}
</script>

<template>

<div>

    <h1>Entrar</h1>

    <input
        v-model="email"
        placeholder="Email"
    />

    <input
        v-model="senha"
        type="password"
        placeholder="Senha"
    />

    <button
        type="button"
        @click="entrar"
    >
        Entrar
    </button>

</div>

</template>