# Frontend — MyEcomerce

SPA Vue 3 que implementa a vitrine pública e o painel administrativo.

## Stack

- Vue 3 + TypeScript
- Vite 8
- Pinia (estado)
- Vue Router 5
- Axios (HTTP)
- Tailwind CSS 4
- PrimeVue 4 + PrimeIcons
- Chart.js (dashboard)

## Estrutura

```
src/
├── api/           # Cliente Axios com JWT
├── assets/        # CSS global
├── components/    # Componentes reutilizáveis
├── pages/         # Páginas por rota
├── router/        # Definição de rotas e guards
├── services/      # Funções de API por domínio
├── stores/        # Stores Pinia
└── types/         # Tipos TypeScript
```

## Configuração

```bash
npm install
```

Variável de ambiente opcional em `.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

## Scripts

| Comando | Descrição |
|---------|-----------|
| `npm run dev` | Servidor de desenvolvimento (porta 5173) |
| `npm run build` | Build de produção com type-check |
| `npm run preview` | Preview do build |
| `npm run lint` | ESLint + Oxlint |
| `npm run format` | Prettier |

## Rotas principais

| Rota | Área | Auth |
|------|------|------|
| `/` | Home | Não |
| `/produtos` | Catálogo | Não |
| `/categoria/:slug` | Catálogo filtrado | Não |
| `/produto/:id` | Detalhe | Não |
| `/sobre` | Sobre a loja | Não |
| `/login` | Login admin | Não |
| `/admin/*` | Painel | JWT obrigatório |

## Stores Pinia

| Store | Responsabilidade |
|-------|------------------|
| `auth` | Login, tokens, estado autenticado |
| `carrinho` | Itens, total, persistência localStorage |
| `loja` | Dados da loja na vitrine |
| `produto` | Listagem e filtros de produtos |
| `categoria` | Categorias |
| `solicitacao` | Pedidos no admin |
| `dashboard` | Métricas do painel |

## Autenticação

Tokens JWT armazenados em `localStorage` (`access`, `refresh`). O interceptor em `api/api.ts` adiciona o Bearer token e renova automaticamente em caso de 401.

## IDE

VS Code com extensão [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar). Desabilite Vetur se estiver instalado.

Documentação completa do projeto: [../docs/README.md](../docs/README.md).
