# Modelo de Entidades

Este documento descreve todas as entidades do sistema, seus atributos e suas responsabilidades.

---

# 🏪 Loja

Representa a identidade visual e as configurações gerais da loja.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador único |
| nome | VARCHAR(120) | Nome da loja |
| descricao | TEXT | Descrição da loja |
| logo | IMAGE | Logo da loja |
| banner_1 | IMAGE | Banner principal |
| banner_2 | IMAGE | Banner secundário |
| banner_3 | IMAGE | Banner opcional |
| banner_4 | IMAGE | Banner opcional |
| telefone | VARCHAR(20) | Telefone para contato |
| whatsapp | VARCHAR(20) | WhatsApp da loja |
| email | VARCHAR(120) | Email |
| instagram | VARCHAR(120) | Instagram |
| facebook | VARCHAR(120) | Facebook |
| pix | VARCHAR(120) | Chave PIX |
| cpf | VARCHAR(14) | CPF do proprietário |
| cnpj | VARCHAR(18) | CNPJ da empresa |
| cep | VARCHAR(9) | CEP |
| rua | VARCHAR(120) | Rua |
| numero | VARCHAR(20) | Número |
| bairro | VARCHAR(80) | Bairro |
| cidade | VARCHAR(80) | Cidade |
| estado | VARCHAR(2) | Estado |
| cor_primaria | VARCHAR(7) | Cor principal da loja |
| cor_secundaria | VARCHAR(7) | Cor secundária |
| mensagem_whatsapp | TEXT | Mensagem padrão enviada ao cliente |
| horario_funcionamento | VARCHAR(120) | Horário da loja |
| ativo | BOOLEAN | Loja ativa |

---

# 📂 Categoria

Organiza os produtos.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador |
| nome | VARCHAR(80) | Nome da categoria |
| descricao | TEXT | Descrição |
| icone | VARCHAR(80) | Ícone (PrimeIcons ou semelhante) |
| ativo | BOOLEAN | Categoria ativa |

---

# 📦 Produto

Representa um produto da loja.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador |
| nome | VARCHAR(120) | Nome |
| descricao | TEXT | Descrição |
| preco | DECIMAL(10,2) | Valor do produto |
| quantidade | INTEGER | Quantidade disponível |
| variacoes | JSON | Tamanhos, cores ou outras variações |
| categoria_id | FK | Categoria do produto |
| destaque | BOOLEAN | Produto em destaque |
| ativo | BOOLEAN | Produto disponível |

---

# 🖼 ImagemProduto

Armazena as imagens dos produtos.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador |
| produto_id | FK | Produto relacionado |
| imagem | IMAGE | Caminho da imagem |
| ordem | INTEGER | Ordem de exibição |

> Regra de negócio: cada produto poderá possuir no máximo **2 imagens**.

---

# 🛒 Solicitação

Representa uma solicitação enviada pelo cliente.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador |
| nome_cliente | VARCHAR(120) | Nome do cliente |
| telefone | VARCHAR(20) | Telefone |
| localizacao | TEXT | Endereço ou localização |
| observacoes | TEXT | Observações |
| valor_total | DECIMAL(10,2) | Valor estimado |
| texto_whatsapp | TEXT | Mensagem gerada automaticamente |
| status | ENUM | Novo, Visto, Concluído ou Cancelado |
| data_criacao | DATETIME | Data da solicitação |

---

# 📄 ItemSolicitação

Representa cada produto presente na solicitação.

| Campo | Tipo | Descrição |
|--------|------|-----------|
| id | INTEGER | Identificador |
| solicitacao_id | FK | Solicitação relacionada |
| produto_id | FK | Produto solicitado |
| quantidade | INTEGER | Quantidade |
| preco_unitario | DECIMAL(10,2) | Valor no momento da solicitação |

---

# 📊 Painel de Controle

O painel administrativo não representa uma entidade do banco de dados.

Ele é uma funcionalidade responsável por consultar as solicitações cadastradas e permitir seu gerenciamento.

## Informações exibidas

| Informação | Origem |
|------------|--------|
| ID | Solicitação |
| Cliente | Solicitação |
| Telefone | Solicitação |
| Quantidade de itens | ItemSolicitação |
| Valor Total | Solicitação |
| Status | Solicitação |
| Data | Solicitação |
| Botão "Detalhes" | Consulta completa da Solicitação |

### Status possíveis

- 🟢 Novo
- 🟡 Visto
- 🔵 Concluído
- 🔴 Cancelado

---

# 🔗 Relacionamentos

```text
Loja
│
├── Categoria
│     │
│     └──── Produto
│              │
│              └──── ImagemProduto
│
└──── Solicitação
         │
         └──── ItemSolicitação
                    │
                    └──── Produto
```

---

# 📌 Resumo das Entidades

| Entidade | Responsabilidade |
|-----------|------------------|
| Loja | Configurações gerais da loja |
| Categoria | Organizar os produtos |
| Produto | Produtos disponíveis |
| ImagemProduto | Imagens dos produtos |
| Solicitação | Solicitações enviadas pelos clientes |
| ItemSolicitação | Produtos pertencentes a uma solicitação |