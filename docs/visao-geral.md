# Catálogo Digital Inteligente
> Um construtor de lojas digitais para pequenos comerciantes.

---

# 📖 Visão do Produto

O **Catálogo Digital Inteligente** é uma plataforma que permite que pequenos comerciantes criem sua própria loja virtual em poucos minutos, sem precisar de conhecimentos técnicos.

Diferente de um e-commerce tradicional, o sistema **não realiza vendas**, **não processa pagamentos** e **não gerencia entregas**.

Seu objetivo é organizar a apresentação dos produtos e facilitar a comunicação entre cliente e vendedor através do WhatsApp e, opcionalmente, disponibilizar uma chave PIX para pagamento.

---

# 🎯 Objetivo

Permitir que qualquer pessoa possa criar uma vitrine digital personalizada para divulgar seus produtos e receber solicitações de compra organizadas.

O foco é simplificar o processo de venda para pequenos comerciantes.

---

# 👥 Público-alvo

O sistema foi pensado para pessoas que vendem pelo WhatsApp ou Instagram.

Exemplos:

- Loja de roupas
- Brechó
- Confeitaria
- Papelaria
- Loja de eletrônicos
- Artesanato
- Cosméticos
- Perfumaria
- Mercado de bairro
- Loja de presentes

---

# 🚫 O que o sistema NÃO é

O projeto não pretende competir com plataformas como Shopify, Nuvemshop ou WooCommerce.

O sistema **não possui**:

- Checkout
- Gateway de pagamento
- Frete
- Rastreamento
- Nota fiscal
- ERP
- Controle financeiro
- Marketplace
- Múltiplos vendedores

Existe apenas **um vendedor**, responsável por toda a administração da loja.

---

# 💡 Problema

Hoje pequenos comerciantes normalmente vendem assim:

Instagram

↓

Cliente pergunta preço

↓

Vendedor envia foto

↓

Cliente pergunta outra coisa

↓

Vendedor procura novamente

↓

Cliente pergunta PIX

↓

Vendedor envia chave

↓

Cliente pergunta endereço

↓

Vendedor envia localização

Todo esse processo é repetitivo e pouco organizado.

---

# ✅ Solução

O sistema organiza toda essa experiência.

O cliente acessa a loja.

↓

Visualiza os produtos.

↓

Escolhe os itens.

↓

Adiciona ao carrinho.

↓

Informa seus dados.

↓

Envia tudo organizado para o WhatsApp do vendedor.

---

# 🛍 Fluxo do Cliente

```text
Entrar na loja

↓

Visualizar produtos

↓

Pesquisar

↓

Filtrar categorias

↓

Adicionar produtos ao carrinho

↓

Escolher quantidade

↓

Informar nome

↓

Informar telefone (opcional)

↓

Informar endereço ou localização

↓

Adicionar observações

↓

Enviar para WhatsApp

↓

Negociação diretamente com o vendedor
```

---

# 🛠 Fluxo do Vendedor

```text
Instalar sistema

↓

Configurar loja

↓

Cadastrar categorias

↓

Cadastrar produtos

↓

Adicionar imagens

↓

Personalizar aparência

↓

Compartilhar link

↓

Receber solicitações pelo WhatsApp
```

---

# 🎨 Personalização da Loja

Cada vendedor poderá personalizar sua loja.

Exemplos:

- Nome
- Logo
- Banner
- Cor principal
- Cor secundária
- Fonte
- Ícone
- WhatsApp
- PIX
- Instagram
- Facebook
- Endereço
- Horário de funcionamento

O objetivo é que cada loja tenha sua própria identidade visual.

---

# 📦 Produtos

Cada produto poderá possuir:

- Nome
- Descrição
- Preço
- Categoria
- Várias imagens
- Produto em destaque
- Disponível ou indisponível

---

# 🗂 Categorias

Exemplos:

- Roupas
- Eletrônicos
- Informática
- Alimentos
- Cosméticos
- Artesanato

---

# 🛒 Carrinho

O carrinho **não representa uma compra**.

Ele apenas organiza os produtos escolhidos pelo cliente.

Sua função é gerar uma solicitação organizada para o vendedor.

---

# 📲 Integração com WhatsApp

Ao finalizar o carrinho o sistema gera automaticamente uma mensagem.

Exemplo:

```text
Olá!

Gostaria de solicitar os seguintes produtos:

• Notebook Dell
Quantidade: 1

• Mouse Logitech
Quantidade: 2

Total estimado:
R$ 4.860,00

Nome:
Luís

Telefone:
(77) XXXXX-XXXX

Endereço:
Rua ...

Observações:
Gostaria de retirar amanhã.
```

Ao confirmar, o WhatsApp é aberto automaticamente com essa mensagem.

---

# 💳 PIX

Opcionalmente o vendedor poderá informar uma chave PIX.

O cliente poderá:

- copiar a chave;
- visualizar um QR Code (futuramente);
- realizar o pagamento diretamente ao vendedor.

O sistema **não confirma pagamentos**.

---

# 🏠 Estrutura Geral

```text
Loja

├── Home
├── Produtos
├── Categorias
├── Carrinho
├── Contato
└── Sobre
```

---

# ⚙ Painel Administrativo

O sistema possui apenas um administrador.

Não existe cadastro de vendedores.

O painel contém:

```text
Dashboard

Produtos

Categorias

Solicitações

Aparência

Configurações
```

---

# 📊 Dashboard

Indicadores simples.

- Produtos cadastrados
- Solicitações recebidas
- Produtos mais visualizados (futuro)
- Produtos em destaque

---

# 🎨 Aparência

O vendedor poderá alterar:

- Logo
- Banner
- Cores
- Tema
- Ícones
- Rodapé
- Redes sociais

---

# 🗃 Banco de Dados

Para manter o sistema simples, será utilizado inicialmente:

- SQLite

Motivos:

- Zero configuração
- Fácil backup
- Banco único em arquivo
- Ideal para pequenos negócios
- Não exige instalação de servidor

Caso o projeto evolua, poderá ser migrado para PostgreSQL.

---

# 🚀 MVP

O MVP será composto por:

## Loja

- Nome
- Logo
- Banner
- Redes sociais
- WhatsApp
- PIX

## Produtos

- CRUD
- Imagens
- Categorias

## Cliente

- Visualização dos produtos
- Pesquisa
- Carrinho

## Solicitação

- Nome
- Telefone
- Endereço
- Observações
- Geração automática da mensagem

## Administração

- Login
- Dashboard
- Produtos
- Categorias
- Aparência
- Configurações

---

# ❌ Funcionalidades Futuras

- Favoritos
- Cupons
- Avaliações
- Chat interno
- Controle de estoque
- Dashboard avançado
- QR Code PIX automático
- Temas prontos
- Exportação de catálogo
- Integração Instagram
- Analytics
- PWA
- Multi-lojas
- Multiusuários

---

# 🏛 Arquitetura

Frontend

- Vue.js
- Tailwind CSS
- PrimeVue

Backend

- Django REST Framework

Banco

- SQLite

Comunicação

- REST API

---

# 🎯 Filosofia do Projeto

> "O sistema não vende.
>
> O sistema organiza a venda."

Nosso objetivo é permitir que qualquer pequeno comerciante tenha uma loja digital bonita, simples e funcional em poucos minutos, sem precisar entender de tecnologia.

O cliente escolhe os produtos.

O sistema organiza a solicitação.

O vendedor fecha a venda da maneira que preferir.