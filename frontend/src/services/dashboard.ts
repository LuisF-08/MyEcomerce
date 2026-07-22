import api from '@/api/api'

export async function dashboard() {
    const response = await api.get("/dashboard/")

    return response.data
}