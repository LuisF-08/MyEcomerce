# Regras de Negócio

## Loja

- Existe apenas uma loja por instalação do sistema.
- Existe apenas um administrador responsável pela loja.
- A loja deve possuir nome e WhatsApp configurados.
- A loja pode possuir uma chave PIX (opcional).
- A identidade visual da loja pode ser personalizada.
- O banner da loja pode conter até 4 imagens.

---

## Produtos

- Todo produto deve pertencer a uma categoria.
- Todo produto deve possuir pelo menos uma imagem.
- Cada produto pode possuir no máximo 2 imagens.
- Produtos podem ser ativados ou desativados.
- Produtos em destaque poderão ser exibidos na página inicial(opcional).

---

## Categorias

- Uma categoria pode possuir vários produtos.
- Um produto pertence a mais de uma categoria.

---

## Carrinho

- O carrinho é temporário.
- O carrinho existe apenas durante a navegação do cliente.
- O cliente pode alterar as quantidades dos produtos.
- O carrinho não representa uma compra.

---

## Cliente

- O cliente não precisa criar uma conta.
- O cliente deverá informar nome antes de enviar a solicitação.
- Telefone é obrigatório.
- Endereço e observações são obrigatória.
- Forma de Pagamento é opcional

---

## Solicitação

- A solicitação será enviada ao vendedor através do WhatsApp.
- O sistema poderá armazenar o histórico das solicitações.
- O sistema não realiza pagamentos.
- O sistema não confirma pagamentos PIX.

___

# **CASOS DE USO**

## Vendedor

- Configurar loja
- Alterar tema
- Alterar banner
- Alterar logo
- Cadastrar categoria
- Editar categoria
- Excluir categoria
- Cadastrar produto
- Editar produto
- Excluir produto
- Visualizar solicitações

---

## Cliente

- Visualizar produtos
- Pesquisar produtos
- Filtrar por categoria
- Adicionar produto ao carrinho
- Alterar quantidade
- Remover produto
- Enviar solicitação pelo WhatsApp