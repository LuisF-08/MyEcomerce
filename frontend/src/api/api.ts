import axios from "axios"

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    headers: {
        "Content-Type": "application/json",
    },
})

// Interceptor de REQUISIÇÃO (Coloca o token em cada chamada)
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access")

    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

//  Interceptor de RESPOSTA (Trata o token expirado)
api.interceptors.response.use(
    (response) => {
        // Se a resposta vier correta (status 2xx), apenas passa adiante
        return response
    },
    async (error) => {
        const originalRequest = error.config

        // Se o erro for 401 e ainda não tentamos refazer esta requisição específica
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true // Evita loop infinito se o refresh também falhar

            try {
                const refreshToken = localStorage.getItem("refresh")
                
                if (!refreshToken) {
                    throw new Error("Nenhum refresh token encontrado.")
                }

                // Faz a chamada para a rota de refresh (geralmente do Simple JWT do Django)
                const response = await axios.post("http://127.0.0.1:8000/api/token/refresh/", {
                    refresh: refreshToken
                })

                const novoAccessToken = response.data.access

                // Salva o novo token de acesso no localStorage
                localStorage.setItem("access", novoAccessToken)

                // Atualiza o cabeçalho da requisição original que falhou com o novo token
                originalRequest.headers.Authorization = `Bearer ${novoAccessToken}`

                // Executa novamente a requisição original e retorna o resultado dela
                return api(originalRequest)
                
            } catch (refreshError) {
                // Se o refresh token também expirou ou falhou, desloga o usuário à força
                localStorage.removeItem("access")
                localStorage.removeItem("refresh")
                
                // Redireciona para o login (recarregando a página limpa o estado)
                window.location.href = "/login"
                return Promise.reject(refreshError)
            }
        }

        // Se for qualquer outro tipo de erro repassa para o componente tratar
        return Promise.reject(error)
    }
)

export default api