# Arquitetura do Projeto

## Arquitetura Geral

```text
Frontend (Vue.js)

        │

 REST API (Django REST Framework)

        │

     SQLite
```

---

# Backend

## Framework

- Django
- Django REST Framework

## Banco de Dados

- SQLite(Como a ideia é ser leve e personalizável ele segue sendo ideal)

## Organização

```text
backend/

apps/

├── core/
├── loja/
├── catalogo/
├── carrinho/
└── solicitacoes/
```

---

# Frontend

## Framework

- Vue.js 3
- TypeScript
- Vite

## Estilização

- Tailwind CSS
- PrimeVue

## Organização

```text
src/

api/

assets/

components/

layouts/

router/

stores/

types/

utils/

views/
```

## Formato de Dashboard
```shell
Dashboard
│
├── Cards
│     ├── Produtos
│     ├── Categorias
│     ├── Pedidos
│     ├── Faturamento
│
├── Gráficos
│     ├── Vendas por mês
│     ├── Pedidos por status
│     ├── Produtos mais vendidos
│
├── Alertas
│     ├── Estoque baixo
│     ├── Produtos inativos
│
└── Tabelas
      ├── Últimos pedidos
      ├── Últimos produtos
```