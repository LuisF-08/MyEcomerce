import api from "@/api/api"

export async function login(
    email: string,
    password: string
) {
    const response = await api.post("/token/", {
        username: email,
        password,
    })

    return response.data
}

export async function me() {
    const response = await api.get("/me")

    return response.data
}

export async function refresh(refreshToken: string){
    const response = await api.post("/token/refresh/", {
        refresh: refreshToken,
    })

    return response.data
}

export function logout() {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
}