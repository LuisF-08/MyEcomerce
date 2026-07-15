# 🛒 *MyEcomerce*

Sistema de catálogo online desenvolvido para pequenos empreendedores que desejam divulgar seus produtos sem a complexidade de um e-commerce tradicional.

O projeto possui um painel administrativo próprio, API REST em Django REST Framework e frontend em Vue.js.

---

# Objetivo

Permitir que pequenas lojas publiquem produtos, recebam pedidos pelo site e gerenciem todas as informações através de um dashboard administrativo.

---

# Tecnologias

## Backend

- Python
- Django
- Django REST Framework
- JWT Authentication
- SQLite (MVP)
- Swagger (drf-spectacular)

## Frontend

- Vue.js
- Vite
- TailwindCSS
- PrimeVue
- Axios

---

# Funcionalidades

## Loja

- Cadastro das informações da loja
- Logo
- Até 4 banners
- Redes sociais
- PIX
- Horário de funcionamento
- Dias de funcionamento
- Personalização de cores

---

## Catálogo

- Cadastro de categorias
- Cadastro de produtos
- Controle de estoque
- Produtos em destaque
- Imagens
- Variações

---

## Solicitações

- Recebimento de pedidos
- Dados do cliente
- Endereço
- Produtos
- Total automático
- Controle de status

---

## Dashboard

- Total de produtos
- Produtos ativos
- Total de categorias
- Pedidos
- Faturamento
- Pedidos por mês
- Produtos mais vendidos
- Últimos pedidos
- Estatísticas financeiras
- Exportação CSV

---

## API

- REST API
- CRUD completo
- JWT Authentication
- Swagger
- Filtros
- Pesquisa
- Ordenação

---

# Estrutura

```
backend/

api/
catalogo/
loja/
solicitacao/
services/

frontend/

views/
components/
pages/
```

---

# Fluxo

Cliente

↓

Visualiza produtos

↓

Seleciona produtos

↓

Envia solicitação

↓

Administrador recebe

↓

Gerencia pelo Dashboard

---

# Segurança

- JWT Authentication
- Permissões por endpoint
- Validações nos serializers
- Administração protegida
- API documentada

---

# Futuras melhorias

- Upload para S3
- Cache com Redis
- Docker
- PostgreSQL
- Celery
- Painel de relatórios
- Analytics
- Cupons
- Avaliações
- Pagamentos online

---

# Autor

**Luís Filipe Moreira Novais**

Bacharelado em Sistemas de Informação — IFBA