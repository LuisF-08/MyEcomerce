export interface Usuario {
    id: number
    username: string
    email: string
}

export interface LoginRequest {
    email: string
    password: string
}

export interface LoginResponse {
    access: string
    refresh: string
    user: Usuario
}

export interface RefreshResponse {

    access: string

}