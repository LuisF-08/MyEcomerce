import { defineStore } from "pinia"
import { ref, computed } from "vue"

import type { Usuario } from "@/types/usuario"

import * as authService from "@/services/auth"

import axios from "axios"

export const useAuthStore = defineStore("auth", () => {

    const usuario = ref<Usuario | null>(null)

    const accessToken = ref(
        localStorage.getItem("access") || ""
    )

    const refreshToken = ref(
        localStorage.getItem("refresh") || ""
    )

    const loading = ref(false)

    async function login(
        email: string,
        password: string
    ) {

        loading.value = true

        try {

            const tokens = await authService.login(
                email,
                password
            )

            accessToken.value = tokens.access
            refreshToken.value = tokens.refresh

            localStorage.setItem(
                "access",
                tokens.access
            )

            localStorage.setItem(
                "refresh",
                tokens.refresh
            )

            usuario.value = await authService.me()

        } finally {

            loading.value = false

        }

    }

    function logout() {

        usuario.value = null

        accessToken.value = ""

        refreshToken.value = ""

        localStorage.removeItem("access")
        localStorage.removeItem("refresh")

    }

    async function carregarUsuario() {

        if (!accessToken.value) {
            return
        }

        try {

            usuario.value =
                await authService.me()

        } catch {

            logout()

        }

    }

    const isAuthenticated = computed(() => {

        return accessToken.value !== ""

    })

    return {

        usuario,

        accessToken,

        refreshToken,

        loading,

        login,

        logout,

        carregarUsuario,

        isAuthenticated

    }

})