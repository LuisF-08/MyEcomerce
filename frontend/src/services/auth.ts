import api from "@/api/api"

import type {
    LoginRequest,
    LoginResponse,
    RefreshResponse
} from "@/types/auth"

export async function login(dados: LoginRequest): Promise<LoginResponse> {
    const response = await api.post<LoginResponse>(
        "/token/",
        dados
    )
    return response.data
}

export async function refreshToken(
    refresh: string
): Promise<RefreshResponse> {

    const response = await api.post<RefreshResponse>(
        "/token/refresh/",
        {
            refresh
        }
    )

    return response.data

}