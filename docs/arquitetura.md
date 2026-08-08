# Arquitetura

## Visão geral

```
┌─────────────────┐     REST/JSON      ┌─────────────────┐
│  Frontend Vue   │ ◄────────────────► │  Backend Django │
│  (porta 5173)   │     JWT Bearer     │  (porta 8000)   │
└─────────────────┘                    └────────┬────────┘
                                                │
                                    ┌───────────┴───────────┐
                                    │                       │
                              ┌─────▼─────┐           ┌─────▼─────┐
                              │  SQLite   │           │   Redis   │
                              │ db.sqlite3│           │  (cache)  │
                              └───────────┘           └───────────┘
```

Comunicação via HTTP. Mídias (imagens) servidas em `/media/` no ambiente de desenvolvimento.

## Backend

### Apps Django

| App | Responsabilidade |
|-----|------------------|
| `loja` | Modelo `Loja` — identidade visual, contato, endereço, horários |
| `catalogo` | Modelos `Categoria` e `Produto` |
| `solicitacao` | Modelos `Solicitacao` e `ItemSolicitacao` |
| `api` | ViewSets, serializers, permissions, `DashboardService` |

Não existem apps `core`, `carrinho` ou `solicitacoes`. O carrinho é exclusivamente frontend.

### Estrutura `backend/api/`

```
api/
├── views/
│   ├── catalogo.py      # CategoriaViewSet, ProdutoViewSet
│   ├── loja.py          # LojaViewSet
│   ├── solicitacao.py   # SolicitacaoViewSet, ItemSolicitacaoViewSet
│   ├── dashboard.py     # DashboardAPIView, ExportarRelatorioCSVView
│   └── usuario.py       # UsuarioView (/api/me)
├── serializers/
├── permissions.py       # AdminOuLeitura, AdminOuCria
└── services/
    └── dashboard.py     # Agregações para o painel
```

### Autenticação e permissões

- Padrão global: `IsAuthenticated` (REST Framework)
- ViewSets sobrescrevem com permissões customizadas:
  - `AdminOuLeitura`: leitura pública; escrita exige `is_staff`
  - `AdminOuCria`: criação de solicitação pública; demais operações exigem admin
- Tokens JWT via `rest_framework_simplejwt`
  - Access: 30 minutos
  - Refresh: 7 dias, com rotação

### Cache

Redis configurado em `settings.CACHES`. Usado no cache de listagens de produtos e categorias (`django.core.cache`).

### Documentação da API

- Schema OpenAPI: `/api/schema/`
- Swagger UI: `/api/docs/`

## Frontend

### Stack

- Vue 3 (Composition API + `<script setup>`)
- TypeScript
- Vite 8
- Pinia (estado global)
- Vue Router 5
- Axios (cliente HTTP com refresh automático de token)
- Tailwind CSS 4 + PrimeVue 4

### Estrutura `frontend/src/`

```
src/
├── api/api.ts           # Instância Axios e interceptors JWT
├── components/
│   ├── cart/            # CarrinhoDrawer
│   ├── catalogo/        # ProdutoCard, ProdutoGrid, CategoriaList
│   ├── common/          # Loading, Empty
│   ├── dashboard/       # Gráficos e cards do admin
│   └── layout/          # Navbar, Footer, layouts cliente/admin
├── pages/
│   ├── client/          # Home, Produtos, Produto, Sobre
│   └── admin/           # Dashboard, Produtos, Categorias, etc.
├── router/index.ts      # Rotas e guard de autenticação
├── services/            # Chamadas à API por domínio
├── stores/              # Pinia: auth, carrinho, produto, loja, etc.
└── types/               # Interfaces TypeScript
```

### Estado do carrinho

Gerenciado pela store Pinia `carrinho`. Persiste em `localStorage` com a chave `"carrinho"`. Não há endpoint de carrinho no backend.

### Variável de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `VITE_API_URL` | `http://localhost:8000/api` | URL base da API |

## Banco de dados

SQLite (`backend/db.sqlite3`). Adequado para instalação single-tenant e deploy simples. Migração para PostgreSQL é possível alterando `DATABASES` em `settings.py`.

## Infraestrutura

`docker/docker-compose.yml` sobe apenas Redis na porta 6379. Backend e frontend rodam localmente fora do Docker.

## Decisões de design

1. **Single-tenant** — uma loja por instalação simplifica modelo e permissões.
2. **Carrinho no cliente** — reduz carga no servidor; pedido só existe após envio (WhatsApp ou POST na API).
3. **WhatsApp como canal** — evita dependência de gateway de pagamento e chat interno.
4. **Snapshot de preço em `ItemSolicitacao`** — preço e nome do produto são copiados no momento do pedido, preservando histórico mesmo se o produto for alterado depois.
