# API REST

Base URL: `http://localhost:8000/api` (desenvolvimento).

Documentação interativa: `http://localhost:8000/api/docs/`

## Autenticação

### Obter tokens

```http
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "senha"
}
```

Resposta:

```json
{
  "access": "<jwt_access>",
  "refresh": "<jwt_refresh>"
}
```

### Renovar access token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<jwt_refresh>"
}
```

### Usar token

Incluir em requisições autenticadas:

```http
Authorization: Bearer <jwt_access>
```

O frontend renova automaticamente o access token quando recebe HTTP 401.

### Usuário logado

```http
GET /api/me
Authorization: Bearer <jwt_access>
```

## Recursos

Todos os recursos abaixo usam o router DRF (`DefaultRouter`). URLs no plural implícito do basename.

### Loja — `/api/loja/`

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/loja/` | Não | Listar lojas |
| GET | `/api/loja/{id}/` | Não | Detalhe |
| POST | `/api/loja/` | Admin | Criar |
| PUT/PATCH | `/api/loja/{id}/` | Admin | Atualizar |
| DELETE | `/api/loja/{id}/` | Admin | Excluir |

Upload de imagens via `multipart/form-data`.

### Categoria — `/api/categoria/`

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/categoria/` | Não | Listar |
| GET | `/api/categoria/{id}/` | Não | Detalhe |
| POST | `/api/categoria/` | Admin | Criar (slug automático) |
| PUT/PATCH | `/api/categoria/{id}/` | Admin | Atualizar |
| DELETE | `/api/categoria/{id}/` | Admin | Excluir |

### Produto — `/api/produto/`

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/produto/` | Não | Listar (com filtros) |
| GET | `/api/produto/{id}/` | Não | Detalhe |
| POST | `/api/produto/` | Admin | Criar |
| PUT/PATCH | `/api/produto/{id}/` | Admin | Atualizar |
| DELETE | `/api/produto/{id}/` | Admin | Excluir |

**Filtros** (`filterset_fields`):

- `categoria`, `ativo`, `destaque` (exact)
- `preco`, `quantidade` (exact, gte, lte)

**Busca** (`search`): `nome`, `descricao`

**Ordenação** (`ordering`): `nome`, `preco`, `quantidade`, `criado_em` (padrão: `-criado_em`)

Listagens usam cache Redis.

### Solicitação — `/api/solicitacao/`

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/solicitacao/` | Admin | Listar |
| GET | `/api/solicitacao/{id}/` | Admin | Detalhe com itens |
| POST | `/api/solicitacao/` | Não | Criar solicitação |
| PUT/PATCH | `/api/solicitacao/{id}/` | Admin | Atualizar |
| DELETE | `/api/solicitacao/{id}/` | Admin | Excluir |
| PATCH | `/api/solicitacao/{id}/status/` | Admin | Alterar status |

Body para alterar status:

```json
{ "status": "VIS" }
```

Valores: `NOV`, `VIS`, `CON`, `CAN`.

### Item de solicitação — `/api/item-solicitacao/`

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/item-solicitacao/` | Admin | Listar |
| GET | `/api/item-solicitacao/{id}/` | Admin | Detalhe |
| POST | `/api/item-solicitacao/` | Admin | Criar item |
| PUT/PATCH | `/api/item-solicitacao/{id}/` | Admin | Atualizar |
| DELETE | `/api/item-solicitacao/{id}/` | Admin | Excluir |

Campos calculados (read-only): `produto_nome`, `preco_unitario`, `subtotal`.

### Dashboard — `/api/dashboard/`

| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| GET | `/api/dashboard/` | Admin | Métricas, gráficos e últimos pedidos |
| GET | `/api/dashboard/exportar-csv/` | Admin | Download CSV de solicitações |

Resposta do dashboard (estrutura resumida):

```json
{
  "cards": {
    "faturamento": 0.0,
    "pedidos_novos": 0,
    "total_pedidos": 0,
    "produto_medio": 0.0
  },
  "pedidos_por_mes": [],
  "produtos_mais_vendidos": [],
  "ultimos_pedidos": []
}
```

## Códigos de resposta comuns

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 201 | Criado |
| 400 | Validação falhou |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Recurso não encontrado |

## Mídia

Imagens uploadadas ficam em `backend/media/` e são servidas em `/media/` quando `DEBUG=True`.

## CORS

Origens permitidas em desenvolvimento: `http://localhost:5173`.

Para produção, atualize `CORS_ALLOWED_ORIGINS` e `ALLOWED_HOSTS` em `backend/backend/settings.py` (via variáveis de ambiente).
