import api from "@/api/api"
import type { DashboardResponse } from "@/types/dashboard"

export async function dashboard(): Promise<DashboardResponse> {

    const response = await api.get<DashboardResponse>(
        "/dashboard/"
    )

    return response.data
}

export async function exportarRelatorioCSV() {
    const response = await api.get('/dashboard/exportar-csv/', {
        responseType: 'blob'
    })
    
    return response.data
}