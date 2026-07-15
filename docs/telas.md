# 📱 Mapeamento de Telas e Melhorias Futuras — MyEcomerce

Este documento detalha o escopo de cada tela do sistema (Site Público e Painel Administrativo) e as melhorias arquiteturais e funcionais projetadas com base no amadurecimento do nosso backend.

---

## 🌐 SITE PÚBLICO (Vitrine do Cliente)

A jornada do cliente é focada em velocidade, clareza visual e fricção zero (sem necessidade de login).

### 🏠 Tela 1 — Home (Apresentação da Loja)
*   **Objetivo:** Capturar a atenção do cliente e apresentar a identidade visual da marca.
*   **Componentes:** Navbar dinâmica, Banner/Carrossel de Banners (configurados na Tela da Loja), Grid de Categorias em Destaque, Vitrine de Produtos em Destaque, Rodapé Informativo.
*   **Funcionalidades:** 
    *   Filtragem por clique nas categorias para recarregar a vitrine.
    *   Barra de busca global reativa por texto.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Lazy Loading de Imagens:** Carregar imagens de produtos apenas quando entrarem no viewport do usuário para melhorar o desempenho em redes móveis (3G/4G).
    *   **Cores do Tema Dinâmicas:** Consumir as variáveis `cor_primaria` e `cor_secundaria` da API para injetar as cores de forma dinâmica no TailwindCSS (usando variáveis CSS no `:root`).

### 📦 Tela 2 — Produtos (Catálogo Geral)
*   **Objetivo:** Exibir todos os itens disponíveis para venda de forma organizada.
*   **Componentes:** Campo de pesquisa textual, Lista lateral de Categorias (com contagem de itens ativos), Cards de Produtos com indicador de preço, Paginação, Seletor de Ordenação (Preço Crescente, Decrescente, Lançamentos).
*   **Funcionalidades:**
    *   Busca cumulativa (ex: Categoria "Bebidas" + busca por "suco").
    *   Atualização reativa da URL para permitir compartilhamento de buscas filtradas (ex: `?categoria=bebidas&busca=suco`).
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Infinite Scroll Opcional:** Substituir a paginação tradicional por carregamento contínuo conforme o usuário rola a tela para baixo.
    *   **Filtros de Faixa de Preço:** Filtro deslizante (slider) dinâmico baseado no menor e maior preço retornados pelo banco.

### 📄 Tela 3 — Detalhes do Produto
*   **Objetivo:** Fornecer todas as informações necessárias para sanar dúvidas e converter o clique em compra.
*   **Componentes:** Galeria de Imagens (Imagem principal + Imagem secundária), Título do Produto, Preço (De/Por se houver promoção), Descrição detalhada, Badge da Categoria, Seletor de Variações (Tamanho, Cor, Sabor), Contador de Quantidade, Botão "Adicionar ao Carrinho".
*   **Funcionalidades:**
    *   Validação em tempo real do estoque do produto ou da variação selecionada.
    *   Alteração dinâmica de imagens com base na variação selecionada.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Variações com Preços Distintos:** Ajustar o modelo de dados para permitir que variações influenciem diretamente no valor final do item (ex: Tamanho P por R$ 50,00 e Tamanho G por R$ 60,00).
    *   **Badge de "Últimas Unidades":** Exibição automática do aviso quando o estoque do produto estiver abaixo de 5 unidades.

### 🛒 Tela 4 — Carrinho
*   **Objetivo:** Permitir que o usuário revise seus produtos, quantidades e valores antes de finalizar a compra.
*   **Componentes:** Tabela/Lista reativa de itens no carrinho, imagem em miniatura, nome do produto e variação escolhida, controles de quantidade individual (`+` e `-`), lixeira para remoção instantânea, card lateral com resumo de subtotal e total.
*   **Funcionalidades:**
    *   Persistência segura do estado do carrinho no `localStorage` do navegador.
    *   Atualização instantânea dos cálculos financeiros sem necessidade de requisição à API.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Verificação de Estoque em Tempo Real no Checkout:** Antes de avançar do carrinho, fazer uma chamada rápida de validação (`POST /api/carrinho/validar-estoque/`) para garantir que os itens no carrinho ainda estão disponíveis fisicamente no banco.

### 📦 Tela 5 — Finalizar Pedido (Checkout)
*   **Objetivo:** Coleta segura de dados cadastrais e endereço de entrega.
*   **Componentes:** Formulário dividido em seções: Dados Pessoais (Nome, Telefone com máscara, E-mail), Endereço (CEP com busca integrada, Rua, Número, Complemento, Bairro, Cidade, Estado), Campo de Observações sobre a Entrega, Resumo do Pedido com Valor Total.
*   **Funcionalidades:**
    *   Busca de CEP integrada à API pública ViaCEP para preenchimento automático do endereço.
    *   Validação estrita de e-mail e telefone antes de habilitar o envio.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Múltiplas Modalidades de Entrega:** Configuração de taxas de entrega fixas por bairro ou faixa de CEP, integrando o valor dinamicamente ao total da solicitação.

### ✅ Tela 6 — Pedido Enviado (Sucesso)
*   **Objetivo:** Confirmar o registro do pedido e direcionar o cliente para o atendimento humano.
*   **Componentes:** Mensagem de sucesso animada (Lottie/SVG), Número Identificador do Pedido, Caixa de Texto contendo a mensagem resumida formatada, Botão de Destaque "Enviar para o WhatsApp".
*   **Funcionalidades:**
    *   Abertura do link do WhatsApp (`https://wa.me/...`) contendo a mensagem detalhada do pedido pré-preenchida (com todos os itens estruturados, subtotal, frete, dados do cliente e endereço de entrega).
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Status de Acompanhamento no WhatsApp:** No texto da mensagem gerada, incluir um link de rastreio direto para o cliente acompanhar o status no site sem precisar de login (ex: `/pedido/status/uuid_do_pedido`).

---

## 🔐 PAINEL ADMINISTRATIVO (Gestão Interna)

Acesso restrito ao lojista. Autenticação mandatória via JWT (`Access` e `Refresh` tokens) em todas as requisições.

### 🔑 Tela 1 — Login
*   **Objetivo:** Autenticação segura do administrador.
*   **Componentes:** Formulário centralizado de credenciais (E-mail e Senha), Opção "Lembrar-me", Botão de Envio.
*   **Funcionalidades:**
    *   Consumo do endpoint `/api/token/` para armazenar de forma segura o `access_token` no estado da aplicação (Pinia) e configurar o `refresh_token` de forma silenciosa.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Recuperação de Senha Segura:** Implementar fluxo de "Esqueci minha senha" enviando token de redefinição com tempo de expiração de 15 minutos para o e-mail do administrador.

### 📊 Tela 2 — Dashboard
*   **Objetivo:** Fornecer inteligência de negócios rápida para tomada de decisões diárias.
*   **Componentes:** 
    *   *Cards Gerenciais:* Faturamento (arredondado/float), Pedidos Novos, Total de Pedidos, Ticket Médio e Média de Produtos por Pedido (calculados de forma reativa pelo Django ORM através do `DashboardService`).
    *   *Gráficos:* Gráfico de linha para faturamento histórico mensal, Gráfico de barras para Produtos Mais Vendidos.
    *   *Seção de Rápido Acesso:* Tabela com os 5 últimos pedidos ordenados por data.
*   **Funcionalidades:**
    *   Agregações dinâmicas usando o modelo `ItemSolicitacao` para o cálculo exato do ticket médio e média física de itens por pedido, sem aproximações.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Filtro por Período Personalizado:** Permitir que o lojista selecione intervalos de datas (Hoje, Últimos 7 dias, Últimos 30 dias, Personalizado) e o backend recalcule todos os cards e gráficos com base no intervalo enviado via query parameters (`?inicio=YYYY-MM-DD&fim=YYYY-MM-DD`).
    *   **Exportação Visual de Relatórios:** Possibilidade de salvar os gráficos em PDF ou PNG diretamente da tela.

### 🛍️ Tela 3 — Produtos (Gerenciador de Estoque)
*   **Objetivo:** Controle central de itens cadastrados.
*   **Componentes:** Tabela de exibição com miniaturas das fotos, preço, categoria correspondente, status ativo/inativo, quantidade atual de estoque, botão de ações rápidas (Editar/Excluir/Mudar Status).
*   **Funcionalidades:**
    *   Busca em tempo real e filtros rápidos por categoria sem recarregar a tela inteira.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Histórico de Alterações de Estoque:** Tela interna para visualizar quem alterou a quantidade de um produto e quando isso aconteceu.
    *   **Alerta de Estoque Baixo Automatizado:** Enviar um e-mail diário ou notificação push no painel listando itens com estoque abaixo do limite mínimo definido.

### ➕ Tela 4 — Novo Produto / Edição
*   **Objetivo:** Cadastro detalhado de novos itens no portfólio.
*   **Componentes:** Campos de texto (Nome, Descrição detalhada), Select de Categoria vinculada, Inputs numéricos (Preço, Quantidade em estoque), Upload de Imagem 1 (Destaque) e Imagem 2, Checkbox de "Produto em Destaque", Checkbox de "Ativo".
*   **Funcionalidades:**
    *   Pré-visualização (preview) das imagens enviadas antes de salvar.
    *   Upload via Multipart form data para o Django persistir as mídias via Pillow.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Upload para Nuvem (S3/Cloudinary):** Substituir o armazenamento de mídia local (`settings.MEDIA_ROOT` no Django) por um serviço de nuvem de alta disponibilidade, o que otimiza custos do servidor.
    *   **Suporte a Múltiplas Variações Avançadas:** Grade de variação flexível onde o lojista cria propriedades customizadas para o produto (ex: Voltagem: 110v/220v).

### 🗂️ Tela 5 — Categorias
*   **Objetivo:** Controle taxonômico dos produtos da loja.
*   **Componentes:** Lista vertical de categorias com indicador de quantidade de produtos que estão associados àquela categoria, modal de adição rápida e edição rápida.
*   **Funcionalidades:**
    *   Bloqueio lógico de exclusão caso a categoria tenha produtos vinculados (evitando registros órfãos no banco de dados).
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Ordenação por Arrastar (Drag & Drop):** Permitir que o lojista altere a ordem em que as categorias aparecem no site público arrastando as caixas na interface.

### 🏪 Tela 6 — Loja (Configurações do Micro SaaS)
*   **Objetivo:** Modificar as informações e a aparência da vitrine do cliente.
*   **Componentes:** Abas separadas por assunto: Informações Básicas, Contato, Redes Sociais, Dados de Pagamento (Chave Pix), Design do Tema (Cores e Banners de Carrossel).
*   **Funcionalidades:**
    *   Persistência central de dados da loja retornados para a aplicação Vue.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Multi-empresa (Multi-tenancy):** Estruturar o banco de dados para suportar múltiplos lojistas independentes no mesmo backend, onde cada usuário do painel administra apenas a sua respectiva loja por ID.

### 📦 Tela 7 — Pedidos (Lista Geral)
*   **Objetivo:** Central de triagem de pedidos recebidos.
*   **Componentes:** Tabela de pedidos com ID, Cliente, Valor Total, Status em destaque (Badges de cores baseadas no status), Data de criação, Botão de visualização detalhada.
*   **Funcionalidades:**
    *   Mecanismo de filtros por Status (`StatusSolicitacao`).
    *   Alteração rápida de status direto na listagem via dropdown.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Atualização de Status em Tempo Real (WebSockets/Django Channels):** Avisar o administrador visualmente e por som a cada novo pedido que entra na fila sem a necessidade de atualizar a página do painel.

### 📄 Tela 8 — Detalhes do Pedido
*   **Objetivo:** Visualização cirúrgica de todos os dados de uma única solicitação para montagem e envio.
*   **Componentes:** Ficha completa do cliente, Quadro de endereço formatado para postagem, Lista de itens comprados (unidades de `ItemSolicitacao` com seus preços unitários e subtotais), Observações e o Dropdown oficial de alteração de status.
*   **Funcionalidades:**
    *   Botão de cópia rápida para área de transferência do texto consolidado do pedido.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Impressão Otimizada:** Folha de estilo CSS de impressão (`@media print`) para imprimir a comanda do pedido formatada especificamente para bobinas de impressoras térmicas (80mm).

### 📈 Tela 9 — Relatórios & Exportações
*   **Objetivo:** Extração de dados históricos de vendas da empresa.
*   **Componentes:** Filtros de período (De/Até), Seletor de Tipo de Relatório (Vendas Gerais, Movimentações de Estoque, Produtos Mais Vendidos), Botão "Exportar para CSV".
*   **Funcionalidades:**
    *   Consumo dinâmico do endpoint `ExportarRelatorioCSVView`, disparando o download nativo do arquivo no navegador do lojista.
*   **🔮 Melhorias Futuras (Frontend & Backend):**
    *   **Exportação em formato PDF:** Integração de bibliotecas Python no backend (como `WeasyPrint` ou `ReportLab`) para renderizar relatórios visualmente elegantes prontos para impressão.