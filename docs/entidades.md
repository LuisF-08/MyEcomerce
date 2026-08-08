# Modelo de dados

Entidades persistidas no SQLite. O carrinho **não** é entidade de banco — vive no `localStorage` do navegador.

## Diagrama de relacionamentos

```
Loja (singleton por instalação)

Categoria ──1:N──► Produto
                      │
                      └──1:N──► ItemSolicitacao ◄──N:1── Solicitacao
```

## Loja

Configurações e identidade visual da loja.

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | BigAutoField | auto | Identificador |
| nome | CharField(120) | sim | Nome da loja |
| descricao | TextField | não | Descrição |
| logo | ImageField | não | Logo |
| banner_1 … banner_4 | ImageField | não | Até 4 banners |
| telefone | CharField(20) | sim | Telefone |
| whatsapp | CharField(20) | sim | WhatsApp (usado no link wa.me) |
| email | EmailField | sim | E-mail |
| instagram | URLField | não | URL do Instagram |
| facebook | URLField | não | URL do Facebook |
| pix | CharField(120) | não | Chave PIX |
| cpf | CharField(14) | sim | CPF do proprietário |
| cnpj | CharField(18) | não | CNPJ |
| cep, rua, numero, referencia, bairro, cidade, estado | — | sim* | Endereço (*referencia opcional) |
| cor_primaria | CharField(7) | sim | Cor hex (#RRGGBB) |
| cor_secundaria | CharField(7) | sim | Cor hex |
| mensagem_whatsapp | TextField | sim | Mensagem padrão (default configurado) |
| horario_funcionamento | TimeField | sim | Abertura |
| horario_fechamento | TimeField | sim | Fechamento |
| dias_funcionamento | CharField(2) | sim | `S` (seg–sex) ou `SS` (seg–sáb) |
| ativo | BooleanField | sim | Loja ativa |
| slug | SlugField | sim | Identificador URL único |
| criado_em, atualizado_em | DateTimeField | auto | Auditoria |

## Categoria

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | BigAutoField | auto | Identificador |
| nome | CharField(200) | sim | Nome |
| slug | SlugField | auto | Gerado a partir do nome |
| descricao | TextField | não | Descrição |
| imagem | ImageField | não | Imagem da categoria |
| ativo | BooleanField | sim | Visível no catálogo |
| ordem | PositiveIntegerField | sim | Ordenação na vitrine |

## Produto

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | BigAutoField | auto | Identificador |
| nome | CharField(100) | sim | Nome |
| descricao | TextField | não | Descrição |
| preco | Decimal(10,2) | sim | Preço unitário |
| quantidade | PositiveIntegerField | sim | Estoque |
| categoria | FK → Categoria | não | Categoria (SET_NULL se removida) |
| imagem_1, imagem_2 | ImageField | não | Até 2 imagens |
| variacoes | JSONField | não | Lista de variações (ex.: tamanhos, cores) |
| ativo | BooleanField | sim | Disponível para venda |
| destaque | BooleanField | sim | Exibir na home |
| criado_em, atualizado_em | DateTimeField | auto | Auditoria |

Não existe modelo `ImagemProduto` separado — imagens ficam no próprio `Produto`.

## Solicitacao

Representa um pedido registrado na API.

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | BigAutoField | auto | Identificador |
| nome | CharField(100) | sim | Nome do cliente |
| telefone | CharField(20) | sim | Telefone |
| email | EmailField | não | E-mail |
| cep | CharField(9) | não | CEP |
| rua, numero, bairro, cidade, estado | — | sim | Endereço |
| referencia | CharField(200) | não | Ponto de referência |
| observacao | TextField | não | Observações |
| total | Decimal(10,2) | auto | Soma dos itens |
| mensagem | TextField | auto | Texto gerado para WhatsApp |
| status | CharField(3) | sim | Ver tabela abaixo |
| criado_em, atualizado_em | DateTimeField | auto | Auditoria |

### Status da solicitação

| Código | Label |
|--------|-------|
| NOV | Novo |
| VIS | Visto |
| CON | Concluído |
| CAN | Cancelado |

Ordenação padrão: mais recente primeiro (`-criado_em`).

## ItemSolicitacao

Itens de uma solicitação. Guarda snapshot do produto no momento do pedido.

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| id | BigAutoField | auto | Identificador |
| solicitacao | FK → Solicitacao | sim | Pedido pai |
| produto | FK → Produto | não | Referência (pode ser nula se produto excluído) |
| produto_nome | CharField(120) | sim | Nome no momento do pedido |
| preco_unitario | Decimal(10,2) | sim | Preço no momento do pedido |
| quantidade | PositiveIntegerField | sim | Quantidade (mínimo 1) |
| subtotal | Decimal(10,2) | sim | preco_unitario × quantidade |
| variacao | CharField(20) | não | Variação escolhida |
| criado_em | DateTimeField | auto | Auditoria |

## Carrinho (frontend)

Interface TypeScript `ItemCarrinho` em `frontend/src/types/carrinho.ts`:

| Campo | Descrição |
|-------|-----------|
| produtoId | ID do produto |
| nome | Nome exibido |
| preco | Preço unitário |
| quantidade | Quantidade selecionada |
| imagem | URL da imagem (opcional) |

Persistido em `localStorage` pela store Pinia `carrinho`.

## Dashboard

Não é entidade de banco. O `DashboardService` agrega dados de `Solicitacao`, `ItemSolicitacao` e `Produto` para:

- Cards: faturamento (pedidos concluídos), pedidos novos, total de pedidos, ticket médio
- Gráfico: pedidos e faturamento por mês
- Ranking: produtos mais vendidos
- Lista: últimos 5 pedidos
- Exportação CSV de todas as solicitações
