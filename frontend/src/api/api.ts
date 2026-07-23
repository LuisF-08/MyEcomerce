import axios from "axios"

// Garante que a URL base nunca termine com barra extra
const rawApiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/api"
const API_URL = rawApiUrl.replace(/\/$/, "")

const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json",
    },
})

// Interceptor de REQUISIÇÃO
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access")

    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

// Interceptor de RESPOSTA
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        // Se der 401 e não for uma tentativa repetida
        if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
            originalRequest._retry = true

            try {
                const refreshToken = localStorage.getItem("refresh")
                
                if (!refreshToken) {
                    throw new Error("Nenhum refresh token encontrado.")
                }

                // Chamada ajustada sem chance de barra duplicada
                const response = await axios.post(`${API_URL}/token/refresh/`, {
                    refresh: refreshToken
                })

                const novoAccessToken = response.data.access

                localStorage.setItem("access", novoAccessToken)

                // Atualiza o header da requisição original
                originalRequest.headers.Authorization = `Bearer ${novoAccessToken}`

                // Refaz a requisição original
                return api(originalRequest)
                
            } catch (refreshError) {
                // Limpa storage
                localStorage.removeItem("access")
                localStorage.removeItem("refresh")
                
                // Redireciona para o caminho CORRETO da tela de login do Admin
                if (window.location.pathname !== "/admin/login") {
                    window.location.href = "/admin/login"
                }
                
                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)

export default api