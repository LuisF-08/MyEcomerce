import { defineStore } from "pinia"
import { computed, ref } from "vue"
import * as authService from "@/services/auth"
import type {
    Usuario,
    LoginRequest
} from "@/types/auth"

export const useAuthStore = defineStore("auth", () => {

    const access = ref<string | null>(
        localStorage.getItem("access")
    )

    const refresh = ref<string | null>(
        localStorage.getItem("refresh")
    )

    const usuario = ref<Usuario | null>(
        JSON.parse(localStorage.getItem("usuario") || "null")
    )

    const loading = ref(false)

    const autenticado = computed(() => !!access.value)

    async function login(dados: LoginRequest) {
        loading.value = true
        try {
            const response = await authService.login(dados)
            access.value = response.access
            refresh.value = response.refresh
            usuario.value = response.user
            localStorage.setItem("access", response.access)
            localStorage.setItem("refresh", response.refresh)
        } catch (error) {
            throw error
        } finally {
            loading.value = false
        }
    
    }

    function logout() {
        access.value = null
        refresh.value = null
        usuario.value = null
        localStorage.removeItem("access")
        localStorage.removeItem("refresh")
        localStorage.removeItem("usuario")
    }

    async function refreshToken() {
        if(!refresh.value) return
        try{
            const response = await authService.refreshToken(
                refresh.value
            )
            access.value = response.access
            localStorage.setItem(
                "access", response.access
            )
        } catch {
            logout()
        }
    }

    return {
        
        access,

        refresh,

        usuario,

        loading,

        autenticado,

        login,

        logout,

        refreshToken

    }

})