/**
 * URL base da API.
 * - Local: VITE_API_URL ou http://localhost:8000/api
 * - Monorepo na Vercel (mesmo domínio): /api
 * - Frontend e backend em projetos Vercel separados: defina VITE_API_URL no painel da Vercel
 */
export function getApiBaseUrl(): string {
    const fromEnv = import.meta.env.VITE_API_URL?.trim()
    if (fromEnv) {
        return fromEnv.replace(/\/$/, "")
    }
    if (import.meta.env.PROD) {
        return "/api"
    }
    return "http://localhost:8000/api"
}

/** Origem do backend (sem /api), para montar URLs de mídia (/media/...) */
export function getBackendOrigin(): string {
    return getApiBaseUrl().replace(/\/api\/?$/, "")
}

/** Converte caminho relativo do Django (/media/...) em URL absoluta */
export function resolveMediaUrl(url?: string | null): string {
    if (!url) return ""
    if (url.startsWith("http") || url.startsWith("data:")) return url
    const origin = getBackendOrigin()
    return `${origin}${url.startsWith("/") ? "" : "/"}${url}`
}
