# Regras de negócio

## Loja

- Uma instalação suporta **uma loja**.
- Um usuário **staff** (superusuário Django) administra o sistema.
- Nome e WhatsApp são obrigatórios para operação da vitrine.
- Chave PIX é opcional.
- Até **4 banners** podem ser cadastrados.
- Cores primária e secundária definem a identidade visual (consumidas pelo frontend).
- Horário de abertura, fechamento e dias de funcionamento são exibidos na vitrine.

## Categorias

- Uma categoria agrupa vários produtos.
- Um produto pertence a **no máximo uma** categoria.
- O slug é gerado automaticamente a partir do nome.
- Categorias inativas não devem aparecer na vitrine pública.
- Exclusão de categoria com produtos vinculados deve ser bloqueada ou tratada (produto fica sem categoria via `SET_NULL`).

## Produtos

- Todo produto deve ter nome e preço.
- Estoque (`quantidade`) é controlado no cadastro; validação de estoque na vitrine depende da implementação do frontend.
- Até **2 imagens** por produto (`imagem_1`, `imagem_2`).
- Produtos inativos não aparecem na vitrine.
- Produtos em destaque aparecem na página inicial.
- Variações são armazenadas como JSON (lista livre); o frontend exibe seletor quando existem variações.

## Carrinho

- Existe apenas no navegador do cliente (`localStorage`).
- Não requer login.
- O cliente pode alterar quantidades e remover itens.
- O carrinho **não é uma compra** — é uma lista temporária para montar a mensagem de pedido.
- Ao enviar pelo WhatsApp, o carrinho é limpo após abrir o link.

## Cliente

- Não precisa criar conta.
- Para enviar pedido via WhatsApp: nome e telefone são esperados pelo formulário do carrinho.
- Endereço e observações são opcionais no fluxo WhatsApp atual.
- Pagamento é acordado diretamente com o vendedor (PIX, dinheiro, etc.).

## Solicitações

- Podem ser criadas via API (`POST /api/solicitacao/`) sem autenticação.
- Apenas administradores podem listar, editar, excluir e alterar status.
- Status segue o fluxo: Novo → Visto → Concluído ou Cancelado.
- O total e a mensagem são calculados/gerados no backend.
- Cada item registra snapshot de nome e preço (`ItemSolicitacao`).
- Faturamento do dashboard considera apenas pedidos com status **Concluído**.
- O sistema **não confirma pagamentos**.

## Permissões da API

| Recurso | Leitura (list/retrieve) | Escrita (create/update/delete) |
|---------|-------------------------|--------------------------------|
| Loja, Produto, Categoria | Público | Admin (`is_staff`) |
| Solicitação | Admin | Create público; demais admin |
| Dashboard, CSV | Admin | Admin |

## Casos de uso

### Administrador

| Ação | Onde |
|------|------|
| Fazer login | `/login` |
| Ver métricas | `/admin` (Dashboard) |
| Gerenciar produtos | `/admin/produtos` |
| Gerenciar categorias | `/admin/categorias` |
| Ver e alterar pedidos | `/admin/solicitacoes` |
| Configurar loja | `/admin/loja` |
| Configurações gerais | `/admin/configuracoes` |
| Exportar CSV | Dashboard → botão exportar |

### Cliente

| Ação | Onde |
|------|------|
| Ver home e destaques | `/` |
| Navegar catálogo | `/produtos`, `/categoria/:slug` |
| Ver detalhe do produto | `/produto/:id` |
| Adicionar ao carrinho | Drawer lateral ou página do produto |
| Finalizar via WhatsApp | Modal no carrinho |
| Ver informações da loja | `/sobre` |
