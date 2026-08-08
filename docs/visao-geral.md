# Visão geral

## O que é

MyEcomerce é um catálogo digital com painel administrativo. Pequenos comerciantes cadastram produtos, personalizam a vitrine e recebem pedidos organizados — normalmente finalizados pelo WhatsApp.

## O que não é

Não é um e-commerce completo. O sistema não oferece:

- Checkout com gateway de pagamento
- Cálculo ou contratação de frete
- Emissão de nota fiscal
- Multi-loja ou multi-vendedor
- Conta de cliente com login

Existe **uma loja** e **um administrador** por instalação.

## Público-alvo

Comerciantes que vendem por WhatsApp, Instagram ou presencialmente e precisam de uma vitrine organizada sem complexidade técnica.

## Problema resolvido

Sem vitrine digital, o atendimento repete as mesmas etapas: enviar fotos, informar preços, repetir chave PIX e endereço. O MyEcomerce centraliza produtos, preços e dados da loja; o cliente monta o pedido e o vendedor recebe tudo estruturado.

## Fluxo do cliente

```
Acessa a loja
    → Navega produtos / categorias
    → Adiciona itens ao carrinho
    → Informa nome, telefone, endereço e observações
    → Envia mensagem pelo WhatsApp
    → Negocia e paga diretamente com o vendedor
```

O carrinho existe apenas no navegador (`localStorage`). Não representa uma compra confirmada.

## Fluxo do administrador

```
Faz login no painel
    → Configura identidade da loja (logo, banners, cores, contatos)
    → Cadastra categorias e produtos
    → Compartilha o link da loja
    → Recebe solicitações (WhatsApp e/ou API)
    → Atualiza status dos pedidos no painel
    → Acompanha métricas no dashboard
```

## Integração com WhatsApp

Ao finalizar o carrinho, o frontend monta uma mensagem com itens, quantidades, total e dados do cliente, e abre o WhatsApp com o texto pré-preenchido. O número de destino vem das configurações da loja (`whatsapp`).

O sistema pode também persistir solicitações na API para histórico e dashboard.

## PIX

A loja pode cadastrar uma chave PIX. O cliente visualiza ou copia a chave na vitrine. O sistema **não confirma** se o pagamento foi realizado.

## MVP implementado

| Módulo | Status |
|--------|--------|
| Configuração da loja | Implementado |
| CRUD de categorias | Implementado |
| CRUD de produtos (imagens, variações, estoque) | Implementado |
| Vitrine pública | Implementado |
| Carrinho com WhatsApp | Implementado |
| Solicitações na API | Implementado |
| Dashboard e exportação CSV | Implementado |
| Cache Redis | Implementado |
| Docker (Redis) | Implementado |

## Fora do escopo atual

Upload para S3, PostgreSQL em produção, recuperação de senha, multi-tenancy, PWA, cupons, avaliações e pagamentos online.
