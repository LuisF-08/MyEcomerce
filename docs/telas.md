# Telas

Mapeamento das rotas implementadas no frontend (`frontend/src/router/index.ts`).

## Site público

Layout: `ClienteLayout.vue`. Sem autenticação.

### Home — `/`

**Arquivo:** `pages/client/Home.vue`

- Banners da loja (até 4)
- Categorias em destaque
- Produtos marcados como destaque
- Navbar com busca e ícone do carrinho

### Catálogo — `/produtos` e `/categoria/:slug`

**Arquivo:** `pages/client/Produtos.vue`

- Listagem de produtos com filtros
- Filtro por categoria via slug na URL
- Busca textual e ordenação via API
- Cards com preço, imagem e botão de adicionar ao carrinho

### Detalhe do produto — `/produto/:id`

**Arquivo:** `pages/client/Produto.vue`

- Galeria (imagem_1 e imagem_2)
- Nome, descrição, preço e categoria
- Seletor de variações (quando `variacoes` não está vazio)
- Controle de quantidade
- Botão "Adicionar ao carrinho"

### Sobre — `/sobre`

**Arquivo:** `pages/client/Sobre.vue`

- Informações da loja: endereço, horários, redes sociais, PIX

### Carrinho (drawer lateral)

**Arquivo:** `components/cart/CarrinhoDrawer.vue`

- Aberto pelo ícone na Navbar
- Lista itens, quantidades e total
- Modal de finalização: nome, telefone, endereço, observações
- Botão abre WhatsApp com mensagem formatada

**Nota:** Existe também `pages/client/Carrinho.vue`, mas a rota `/carrinho` não está registrada no router. O fluxo principal usa o drawer.

---

## Painel administrativo

Layout: `AdminLayout.vue`. Rotas protegidas por JWT (`meta.requiresAuth`).

### Login — `/login`

**Arquivo:** `pages/admin/LoginAdmin.vue`

- Formulário e-mail/senha
- Obtém tokens em `POST /api/token/`
- Armazena `access` e `refresh` no `localStorage`

### Dashboard — `/admin`

**Arquivo:** `pages/admin/DashboardAdmin.vue`

- Cards: faturamento, pedidos novos, total de pedidos, ticket médio
- Gráficos: vendas por mês, pedidos por status, produtos mais vendidos
- Tabela dos últimos pedidos
- Exportação CSV (`GET /api/dashboard/exportar-csv/`)

### Produtos — `/admin/produtos`

**Arquivo:** `pages/admin/ProdutosAdmin.vue`

- Listagem com busca e filtros
- Criar, editar e excluir produtos
- Upload de imagens, controle de estoque, destaque e status ativo

### Categorias — `/admin/categorias`

**Arquivo:** `pages/admin/CategoriaAdmin.vue`

- CRUD de categorias
- Ordenação e status ativo/inativo

### Solicitações — `/admin/solicitacoes`

**Arquivo:** `pages/admin/SolicitacoesAdmin.vue`

- Listagem de pedidos com status
- Filtro por status
- Alteração de status (`PATCH /api/solicitacao/{id}/status/`)
- Visualização de itens e dados do cliente

### Loja — `/admin/loja`

**Arquivo:** `pages/admin/LojaAdmin.vue`

- Nome, descrição, logo e banners
- Contatos: telefone, WhatsApp, e-mail, redes sociais
- Endereço completo
- Cores, horários e dias de funcionamento
- Chave PIX

### Configurações — `/admin/configuracoes`

**Arquivo:** `pages/admin/ConfiguracaoAdmin.vue`

- Configurações complementares da conta e da aplicação

---

## Componentes compartilhados relevantes

| Componente | Função |
|------------|--------|
| `Navbar.vue` | Navegação, busca, carrinho |
| `Footer.vue` | Links e informações |
| `Sidebar.vue` | Menu lateral do admin |
| `ProdutoCard.vue` | Card de produto na vitrine |
| `ProdutoGrid.vue` | Grid responsivo de produtos |
| `CategoriaList.vue` | Lista de categorias |
| `GraficoVendas.vue` | Gráfico de linha (Chart.js) |
| `GraficoPedidos.vue` | Gráfico de barras por status |
| `ResumoCard.vue` | Card numérico do dashboard |
| `UltimosPedidos.vue` | Tabela resumida de pedidos |
| `Loading.vue` / `Empty.vue` | Estados de carregamento e vazio |
