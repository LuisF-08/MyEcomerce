## API PAGAMENTO (MERCADO PAGO)

Documentação da integração de pagamento online com o **Checkout Pro** do Mercado Pago: o cliente é redirecionado para a página de pagamento do Mercado Pago, e os dados de cartão **nunca** passam pelo nosso sistema.

---

### 1. Visão geral

**Princípio central:** o servidor decide tudo que envolve dinheiro. O navegador apenas pede.

| O que | Quem decide |
|---|---|
| Preço de cada produto e total do pedido | Banco de dados (backend) |
| Status do pedido | Backend |
| Se o pagamento foi aprovado | API do Mercado Pago, consultada pelo backend |
| Para onde o cliente vai pagar | Link gerado pelo backend |

O frontend nunca envia preços e nunca decide se um pagamento foi aprovado.

---

### 2. Fluxo completo

```
 FRONTEND                         BACKEND                            MERCADO PAGO
 ────────                         ───────                            ────────────
 1. Cliente clica em
    "Pagar com Mercado Pago",
    preenche nome e telefone
        │
        ├── POST /api/checkout/ ──► Cria Solicitacao (status AGP)
        │   { dados + itens }       e ItemSolicitacao, com preços
        │                           e total lidos do BANCO
        │◄── { id, total, status } ─┘
        │
        ├── POST /api/pagamentos/criar/ ─► Valida que o pedido está em AGP
        │   { solicitacao: id }          Monta os itens a partir do banco
        │                                ├── cria preferência ─────────► Gera o link
        │                                │◄── preference_id + init_point ┘
        │                                Salva Pagamento (pendente)
        │◄── { pagamento_id, init_point }┘
        │
 2. window.location.href = init_point ─────────────────────────────► Cliente paga
        │                                                              na página do MP
        │◄──────────── redireciona para /pagamento/retorno?payment_id=... ──┘
        │
 3. Tela de retorno lê o payment_id
        │
        ├── POST /api/pagamentos/confirmar/ ─► Consulta o pagamento ──► Devolve o estado real
        │   { payment_id }                     Confere o valor pago
        │                                      Atualiza Pagamento
        │                                      AGP → NOV se aprovado
        │◄── { status, solicitacao } ────────┘
        │
 4. Mostra "aprovado / pendente / recusado"
    e limpa o carrinho se aprovado
```

> **Ainda não implementado:** webhook. Hoje o pedido só é confirmado quando o cliente **volta ao site**. Veja a seção 11.

---

### 3. Estrutura de arquivos

```
backend/
├── pagamento/
│   └── models.py                  # model Pagamento
├── solicitacao/
│   └── models.py                  # Solicitacao, ItemSolicitacao, StatusSolicitacao
└── api/
    ├── services/
    │   ├── pagamento.py           # ÚNICO arquivo que fala com o Mercado Pago
    │   └── concilia.py            # liga o resultado do MP ao nosso banco
    ├── serializers/
    │   ├── pagamento.py           # valida entradas de criar/confirmar
    │   └── solicitacao.py         # CheckoutSerializer (cria pedido seguro)
    ├── views/
    │   ├── pagamento.py           # CriarPagamentoView, ConfirmarPagamentoView
    │   └── solicitacao.py         # CheckoutView
    └── urls.py                    # rotas

frontend/src/
├── types/pagamento.ts             # tipos TypeScript das requisições/respostas
├── services/pagamento.ts          # chamadas HTTP ao nosso backend
├── composables/usePagamento.ts    # lógica reutilizável do botão de pagar
├── components/cart/CarrinhoDrawer.vue
├── pages/client/PagamentoRetorno.vue
└── router/index.ts                # rota /pagamento/retorno
```

**Regra de responsabilidade:** cada camada só conhece a de baixo.

- `View` valida e orquestra, não sabe falar com o Mercado Pago.
- `Service` fala com o Mercado Pago, não sabe nada de HTTP nem de Django REST.
- No frontend, o componente só mostra a tela; quem decide os passos é o composable, e quem fala com a API é o service.

Se um dia o gateway mudar, apenas `api/services/pagamento.py` precisa ser reescrito.

---

### 4. Configuração

#### Variáveis de ambiente

| Variável | Para que serve |
|---|---|
| `MERCADOPAGO_ACCESS_TOKEN` | Token do vendedor. Autentica o backend no Mercado Pago. **Secreto.** |
| `MERCADOPAGO_WEBHOOK_SECRET` | Chave para validar a assinatura do webhook (reservado para o webhook). **Secreto.** |
| `FRONTEND_URL` | URL do frontend, usada para montar as URLs de retorno (sem barra no final). |

Em desenvolvimento ficam em `payment.env`, na raiz do repositório. Em produção, no painel da Vercel.

```dotenv
MERCADOPAGO_ACCESS_TOKEN=...
MERCADOPAGO_WEBHOOK_SECRET=...
FRONTEND_URL=http://localhost:5173
```

> `payment.env` **nunca** pode ser versionado. Confirme que está no `.gitignore`. O `.env.example` deve ter só os nomes, sem valores.

#### `settings.py`

```python
load_dotenv(BASE_DIR.parent / "payment.env")   # carrega o arquivo na raiz do repo

MERCADOPAGO_ACCESS_TOKEN = os.environ.get("MERCADOPAGO_ACCESS_TOKEN", "")
MERCADOPAGO_WEBHOOK_SECRET = os.environ.get("MERCADOPAGO_WEBHOOK_SECRET", "")
```

- `load_dotenv` lê o arquivo `.env` e coloca cada linha no ambiente do processo.
- `os.environ.get("NOME", "")` lê uma variável do ambiente e devolve `""` se ela não existir.
- Os apps `pagamento` e `solicitacao` precisam estar em `INSTALLED_APPS`.

#### Credenciais de teste x produção

O código é o **mesmo** nos dois ambientes. O que muda é o token:

- Token de **usuário de teste**: cria pagamentos de mentira. Só aceita pagar um **comprador de teste**.
- Token de **produção**: cria pagamentos reais.

---

### 5. Backend, arquivo por arquivo

#### 5.1 `solicitacao/models.py`: o pedido

```python
class StatusSolicitacao(models.TextChoices):
    AGUARDANDO_PAGAMENTO = "AGP", "Aguardando pagamento"
    NOVO = "NOV", "Novo"
    ...
```

- `TextChoices` cria uma lista de opções fixas. O primeiro valor (`"AGP"`) é o que vai para o banco, e o segundo é o texto exibido.
- Acesso no código: `StatusSolicitacao.AGUARDANDO_PAGAMENTO`.

**Ciclo de vida do pedido:**

| Status | Significado |
|---|---|
| `AGP` | Criado, aguardando pagamento. Não aparece como venda. |
| `NOV` | Pago (ou pedido normal). Entra no fluxo do admin. |
| `VIS` / `CON` / `CAN` | Visto, concluído, cancelado. |

Os campos de endereço (`rua`, `numero`, `bairro`, `cidade`, `estado`) têm `blank=True`: o formulário do carrinho coleta um endereço livre, que é gravado no campo `rua`.

#### 5.2 `pagamento/models.py`: cada tentativa de pagamento

```python
class Pagamento(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        APROVADO = "aprovado", "Aprovado"
        ...

    solicitacao = models.ForeignKey("solicitacao.Solicitacao", on_delete=models.PROTECT, related_name="pagamentos")
    preference_id = models.CharField(max_length=100, blank=True)
    mp_payment_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
```

| Campo | Para que serve |
|---|---|
| `solicitacao` | Liga o pagamento ao pedido. `ForeignKey` = "este pagamento pertence a um pedido". |
| `on_delete=PROTECT` | Impede apagar um pedido que tem pagamento registrado. |
| `related_name="pagamentos"` | Permite `solicitacao.pagamentos.all()`. |
| `preference_id` | Id do "link de pagamento" criado no Mercado Pago. |
| `mp_payment_id` | Id do pagamento de fato. Só existe depois que o cliente paga. |
| `unique=True` | O mesmo pagamento não pode ser registrado duas vezes. |
| `null=True` | Ao criar o link, o `mp_payment_id` ainda não existe. |
| `valor` | Valor cobrado nessa tentativa (cópia do total do pedido). |

Um pedido pode ter **vários** pagamentos (tentativas), por isso é uma tabela separada.

`DecimalField` é usado para dinheiro porque não tem os erros de arredondamento do `float`.

#### 5.3 `api/services/pagamento.py`: fala com o Mercado Pago

```python
def _sdk():
    return mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
```

Cria o cliente do Mercado Pago. O `_` no início é convenção: "uso interno do arquivo".

```python
def criar_preferencia(*, itens, external_reference):
```

- O `*,` obriga a chamar com nomes: `criar_preferencia(itens=..., external_reference=...)`. Evita trocar argumentos de lugar.
- **Preferência** é o "carrinho" que o Mercado Pago exibe na página de pagamento.

O corpo enviado:

```python
corpo = {
    "items": [ {...} for i in itens ],
    "external_reference": str(external_reference),
    "back_urls": { "success": ..., "failure": ..., "pending": ... },
    "auto_return": "approved",
}
```

- `[ {...} for i in itens ]` é uma **list comprehension**: cria uma lista transformando cada item de `itens`.
- `external_reference` é a ponte entre os dois sistemas: guardamos o **id da solicitação**, e o Mercado Pago o devolve quando falar de um pagamento.
- `back_urls`: para onde o cliente volta depois de pagar.
- `auto_return: "approved"`: volta sozinho ao site se aprovado.

```python
resposta = _sdk().preference().create(corpo)
if resposta["status"] not in (200, 201):
    raise ErroMercadoPago(resposta.get("response"))
dados = resposta["response"]
return {"preference_id": dados["id"], "init_point": dados["init_point"]}
```

- `init_point` é a URL da página de pagamento.
- `raise ErroMercadoPago(...)` interrompe a função com um erro **nosso**, que a view sabe tratar.

`consultar_pagamento(payment_id)` pergunta ao Mercado Pago o estado real de um pagamento.

#### 5.4 `api/services/concilia.py`: a conciliação

"Conciliar" = fazer o nosso banco refletir o que o Mercado Pago diz.

```python
STATUS_MP = {
    "approved": Pagamento.Status.APROVADO,
    "pending": Pagamento.Status.PENDENTE,
    "in_process": Pagamento.Status.PENDENTE,
    "authorized": Pagamento.Status.PENDENTE,
    "rejected": Pagamento.Status.RECUSADO,
    "cancelled": Pagamento.Status.CANCELADO,
    "refunded": Pagamento.Status.ESTORNADO,
    "charged_back": Pagamento.Status.ESTORNADO,
}
```

Dicionário que **traduz** os status do Mercado Pago para os nossos.

```python
@transaction.atomic
def conciliar_pagamento(payment_id):
```

- `@transaction.atomic` é um **decorator**: tudo dentro da função acontece como uma unidade. Se algo falhar no meio, nada é gravado.

Passo a passo da função:

1. `dados = consultar_pagamento(payment_id)` pergunta ao Mercado Pago.
2. `Solicitacao.objects.select_for_update().get(pk=dados.get("external_reference"))` localiza o pedido pelo `external_reference` e **trava a linha** no banco, para duas chamadas simultâneas não se atropelarem.
3. `Decimal(str(dados["transaction_amount"])) != solicitacao.total` confere se o valor pago é o valor do pedido. Se não for, lança `PagamentoInvalido`.
4. `novo_status = STATUS_MP.get(dados["status"], PENDENTE)` traduz o status. Status desconhecido vira "pendente".
5. Escolhe o registro de `Pagamento` a atualizar, nesta ordem:
   ```python
   pagamento = (
       registro_com_este_payment_id
       or ultima_tentativa_pendente_do_pedido
       or novo_registro
   )
   ```
   O `or` devolve o primeiro valor que **não for vazio**. `.first()` devolve o primeiro resultado ou `None`.
6. Grava `mp_payment_id` e `status`.
7. Só libera o pedido se estava em `AGP` **e** o pagamento foi aprovado: `AGP → NOV`.

**Idempotência:** chamar a função duas vezes com o mesmo `payment_id` dá o mesmo resultado, sem duplicar nada. Isso protege contra recarregar a página de retorno, e contra o futuro webhook chegando junto com o retorno do cliente.

`PagamentoInvalido` é uma exceção própria: `class PagamentoInvalido(Exception): pass`.

#### 5.5 Serializers

**`CheckoutSerializer`** (`api/serializers/solicitacao.py`) cria o pedido com segurança:

```python
class ItemCheckoutSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.all())
    quantidade = serializers.IntegerField(min_value=1, max_value=99)
    variacao = serializers.CharField(required=False, allow_blank=True, max_length=20)
```

- O cliente só envia **qual produto** e **quantas unidades**.
- `PrimaryKeyRelatedField` valida que o produto existe e já entrega o objeto `Produto`.

```python
class CheckoutSerializer(serializers.ModelSerializer):
    itens = ItemCheckoutSerializer(many=True, write_only=True, allow_empty=False)
    class Meta:
        read_only_fields = ["id", "total", "status"]
```

- `read_only_fields`: o cliente **não consegue** enviar `total` nem `status`. Ficar só leitura é o que impede alguém de mandar `"status": "CON"`.
- `write_only=True` em `itens`: aceita na entrada, não devolve na resposta.
- `allow_empty=False`: pedido sem itens é rejeitado.

```python
@transaction.atomic
def create(self, validated_data):
    itens_data = validated_data.pop("itens")
    solicitacao = Solicitacao.objects.create(total=0, status=AGUARDANDO_PAGAMENTO, **validated_data)
    for item in itens_data:
        subtotal = produto.preco * item["quantidade"]   # preço vem do BANCO
        ItemSolicitacao.objects.create(...)
        total += subtotal
    solicitacao.total = total
```

- `validated_data` são os dados já validados.
- `**validated_data` "espalha" o dicionário como argumentos nomeados.
- O pedido nasce em `AGP`, o preço vem de `produto.preco`, e o total é somado no servidor.
- `@transaction.atomic`: se um item falhar, o pedido inteiro é desfeito.

**`CriarPagamentoSerializer`** valida `{"solicitacao": 13}`:

```python
solicitacao = serializers.PrimaryKeyRelatedField(queryset=Solicitacao.objects.all())
```

**`ConfirmarPagamentoSerializer`** valida `{"payment_id": "123"}`:

```python
payment_id = serializers.RegexField(r"^\d{1,20}$")
```

`^\d{1,20}$` significa "de 1 a 20 dígitos, e nada além disso". Impede que texto estranho vá para a chamada externa.

#### 5.6 Views

Todas as três são **públicas** (o cliente não tem login) e ignoram qualquer token:

```python
authentication_classes = []
permission_classes = [AllowAny]
```

> Sem `authentication_classes = []`, o DRF valida o token JWT mesmo em rota pública. Um token de admin vencido no navegador derrubaria o cliente com erro 401.

**`CheckoutView`** (em `views/solicitacao.py`): `generics.CreateAPIView` com o `CheckoutSerializer`. Cria o pedido.

**`CriarPagamentoView`:**

1. `serializer.is_valid(raise_exception=True)`: se inválido, responde 400 automaticamente.
2. `solicitacao.status != AGUARDANDO_PAGAMENTO` → 400. Só gera link para pedido que realmente aguarda pagamento.
3. Monta `itens` lendo `solicitacao.itens.all()` (banco), nunca a requisição.
4. `criar_preferencia(...)` dentro de `try/except ErroMercadoPago` → 502 se o Mercado Pago falhar.
5. Salva um `Pagamento` pendente com o `preference_id`.
6. Responde `201` com `pagamento_id` e `init_point`.

**`ConfirmarPagamentoView`:** valida o `payment_id` e chama `conciliar_pagamento`. Trata dois erros: `PagamentoInvalido` → 400, `ErroMercadoPago` → 502.

**Permissões do admin:** `SolicitacaoViewSet` e `ItemSolicitacaoViewSet` usam `IsAdminUser`. Visitante **não** pode criar, editar nem listar pedidos por elas, apenas pelo `/checkout/`.

#### 5.7 `api/urls.py`

```python
path('checkout/', CheckoutView.as_view(), name='checkout'),
path('pagamentos/criar/', CriarPagamentoView.as_view(), name='pagamento-criar'),
path('pagamentos/confirmar/', ConfirmarPagamentoView.as_view(), name='pagamento-confirmar'),
```

`.as_view()` converte a classe em uma função que o Django consegue chamar.

---

### 6. Referência dos endpoints

Todos sob `/api/`, públicos.

#### `POST /api/checkout/`: cria o pedido

```json
{
  "nome": "Maria Silva",
  "telefone": "11999999999",
  "rua": "Rua A, 10, Centro",
  "observacao": "Tamanho M",
  "itens": [{ "produto": 1, "quantidade": 2, "variacao": "M" }]
}
```

| Campo | Obrigatório |
|---|---|
| `nome`, `telefone`, `itens` | Sim |
| `email`, `cep`, `rua`, `numero`, `referencia`, `bairro`, `cidade`, `estado`, `observacao` | Não |
| `itens[].produto`, `itens[].quantidade` (1 a 99) | Sim |
| `itens[].variacao` | Não |

**201:** `{ "id": 13, "nome": "...", "total": "99.80", "status": "AGP", ... }`
**400:** campo inválido, produto inexistente ou lista de itens vazia.

#### `POST /api/pagamentos/criar/`: gera o link

```json
{ "solicitacao": 13 }
```

**201:** `{ "pagamento_id": 1, "init_point": "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=..." }`
**400:** pedido inexistente, ou que não está em `AGP`.
**502:** o Mercado Pago recusou ou está indisponível.

#### `POST /api/pagamentos/confirmar/`: confirma o pagamento

```json
{ "payment_id": "123456789" }
```

**200:** `{ "status": "aprovado", "solicitacao": 13 }`
**400:** `payment_id` inválido, pedido não encontrado ou valor divergente.
**502:** falha ao consultar o Mercado Pago.

---

### 7. Frontend, arquivo por arquivo

#### 7.1 `types/pagamento.ts`: os "contratos"

```ts
export interface CheckoutPayload {
  nome: string
  telefone: string
  rua?: string
  itens: ItemCheckout[]
}

export type StatusPagamento = 'pendente' | 'aprovado' | 'recusado' | 'cancelado' | 'estornado'
```

- `interface` descreve o formato de um objeto. O `?` marca o campo como opcional.
- `type X = 'a' | 'b'` é uma união: o valor só pode ser um dos listados. O editor avisa se você digitar errado.
- `export` permite importar em outros arquivos.

Os tipos só existem na hora de escrever o código: o TypeScript os apaga ao compilar.

#### 7.2 `services/pagamento.ts`: as chamadas HTTP

```ts
export async function criarPagamento(solicitacaoId: number): Promise<CriarPagamentoResposta> {
  const response = await api.post<CriarPagamentoResposta>('/pagamentos/criar/', { solicitacao: solicitacaoId })
  return response.data
}
```

- `async` marca uma função que faz algo demorado (rede) e devolve uma **Promise**.
- `await` espera o resultado antes de continuar.
- `Promise<X>` diz "isto vai devolver um X no futuro".
- `api.post<X>(...)` usa um **genérico**: informa ao TypeScript o formato da resposta, e assim `response.data` tem tipo.
- `api` é a instância do axios (`api/api.ts`), que já sabe a URL base e anexa o token quando existe.

Funções: `criarCheckout`, `criarPagamento`, `confirmarPagamento`. O frontend **só** fala com o nosso backend, nunca com o Mercado Pago.

#### 7.3 `composables/usePagamento.ts`: a lógica reutilizável

Um **composable** é uma função do Vue que agrupa estado e lógica para reaproveitar em vários componentes.

```ts
export function usePagamento() {
  const carrinho = useCarrinhoStore()
  const carregando = ref(false)
  const erro = ref('')

  async function pagarMercadoPago(cliente: DadosCliente) { ... }

  return { carregando, erro, pagarMercadoPago }
}
```

- `ref(valor)` cria um valor **reativo**: quando muda, a tela atualiza. Acesse com `.value` no script.
- O `return` final expõe o que o componente pode usar.

O passo a passo de `pagarMercadoPago`:

1. `if (carregando.value) return`: evita duplo clique.
2. Se o carrinho está vazio, mostra erro e para.
3. `carregando.value = true`.
4. **Cria o pedido**, mandando apenas `produto` e `quantidade`:
   ```ts
   itens: carrinho.itens.map((item) => ({
     produto: item.produtoId,
     quantidade: item.quantidade,
     ...(item.variacao ? { variacao: item.variacao } : {}),
   }))
   ```
   - `.map()` transforma cada item do carrinho em um item do pedido.
   - `...(condição ? { x } : {})` é o **spread condicional**: só inclui `variacao` se ela existir.
   - `cliente.endereco?.trim() ?? ''`: o `?.` (optional chaining) só chama `.trim()` se o valor existir, e o `??` usa `''` se o resultado for `null` ou `undefined`.
5. **Gera o link**: `criarPagamento(pedido.id)`.
6. `window.location.href = pagamento.init_point` redireciona o navegador.
7. No `catch`, mostra o erro e libera o botão.

Detalhes de projeto:

- O `carregando` continua `true` em caso de sucesso **de propósito**: o navegador está saindo da página.
- O carrinho **não** é limpo aqui. Só será limpo na tela de retorno, quando o backend confirmar. Quem desistir no Mercado Pago volta com o carrinho intacto.

#### 7.4 `components/cart/CarrinhoDrawer.vue`

```ts
const { carregando: carregandoMp, erro, pagarMercadoPago: iniciarPagamento } = usePagamento()
```

- **Desestruturação com renomeação**: `carregando: carregandoMp` pega a propriedade `carregando` e a chama de `carregandoMp` neste componente.

O mesmo modal serve para WhatsApp e Mercado Pago:

```ts
type Modo = 'whatsapp' | 'mercadopago'
const modo = ref<Modo>('whatsapp')
function abrirModal(m: Modo) { modo.value = m; erro.value = ''; showModal.value = true }
```

- `ref<Modo>(...)` informa o tipo do valor reativo.
- No template, `v-if="modo === 'whatsapp'"` escolhe qual botão aparece, e `:disabled="!nome || !telefone || carregandoMp"` impede enviar sem os dados ou clicar duas vezes.

#### 7.5 `pages/client/PagamentoRetorno.vue`: a tela de volta

O Mercado Pago devolve o cliente em `/pagamento/retorno?payment_id=...&status=approved&...`.

```ts
const bruto = route.query.payment_id ?? route.query.collection_id
const paymentId = String((Array.isArray(bruto) ? bruto[0] : bruto) ?? '')
if (!/^\d{1,20}$/.test(paymentId)) { estado.value = 'erro'; return }
const resposta = await confirmarPagamento(paymentId)
```

- `route.query` lê os parâmetros da URL.
- A tela **ignora** o `?status=approved` da URL (qualquer um pode digitar isso). Ela só extrai o `payment_id`, valida o formato e **pergunta ao backend**.
- Se o backend confirmar `aprovado`, chama `carrinho.limpar()`.
- `onMounted(async () => {...})` roda quando a tela é aberta.
- O `computed` `visual` escolhe ícone, cor e texto de acordo com o estado.

Estados exibidos: carregando, aprovado, pendente, recusado, cancelado, estornado e erro.

#### 7.6 `router/index.ts`

```ts
{ path: "pagamento/retorno", name: "pagamento-retorno", component: () => import("@/pages/client/PagamentoRetorno.vue") }
```

O `path` precisa ser **idêntico** ao usado em `back_urls` no backend (`/pagamento/retorno`). `() => import(...)` carrega a tela só quando a rota é visitada (lazy loading).

---

### 8. Status: como tudo se conecta

| Mercado Pago | `Pagamento.status` | Efeito no pedido |
|---|---|---|
| `approved` | `aprovado` | `AGP → NOV` |
| `pending`, `in_process`, `authorized` | `pendente` | continua `AGP` |
| `rejected` | `recusado` | continua `AGP` |
| `cancelled` | `cancelado` | continua `AGP` |
| `refunded`, `charged_back` | `estornado` | não altera automaticamente |

---

### 9. Segurança: o que cada decisão evita

| Decisão | Fraude ou falha que evita |
|---|---|
| Frontend envia só `produto` e `quantidade`; preço vem do banco | Alterar o preço no navegador |
| `total` e `status` são `read_only` no `CheckoutSerializer` | Criar pedido já como "Concluído" |
| `SolicitacaoViewSet` com `IsAdminUser` | Visitante criar ou editar pedidos |
| `/pagamentos/criar/` só aceita pedido em `AGP` | Gerar link de pedido já pago ou cancelado |
| Confirmação consulta a API do Mercado Pago | Forjar `?status=approved` na URL de retorno |
| Conferência `transaction_amount == total` | Pagamento de valor menor aceito |
| `mp_payment_id` com `unique=True` | Processar o mesmo pagamento duas vezes |
| `@transaction.atomic` + `select_for_update` | Pedido pela metade, ou duas confirmações simultâneas |
| Token só no backend, em variável de ambiente | Vazar a credencial |
| Regex no `payment_id` | Texto arbitrário indo para chamada externa |
| `authentication_classes = []` nas views públicas | Token expirado derrubando o cliente |

---

### 10. Como testar

**Pré-requisitos locais**

1. `payment.env` com `FRONTEND_URL=http://localhost:5173`. Reinicie o backend após alterar.
2. Backend em `http://localhost:8000` e frontend em `http://localhost:5173`.
3. Em teste local, se a criação do link falhar por causa do `auto_return` com `localhost`, comente essa linha em `api/services/pagamento.py` apenas durante o teste.

**Teste pelo navegador**

1. Adicione um produto ao carrinho, clique em **Pagar com Mercado Pago**, preencha nome e telefone e confirme.
2. Na página do Mercado Pago, use uma **janela anônima**, entre com o **comprador de teste** e pague com um cartão de teste (lista em `cartoes.md`).
3. Ao voltar, a tela deve mostrar "Pagamento aprovado!" e o carrinho deve esvaziar.
4. No admin, o pedido deve estar como "Novo" e deve existir um `Pagamento` aprovado.

**Teste pelo terminal**

```bash
# 1. cria o pedido
curl -X POST http://localhost:8000/api/checkout/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","telefone":"11999999999","rua":"Rua A, 10","itens":[{"produto":1,"quantidade":2}]}'

# 2. gera o link (use o "id" devolvido acima)
curl -X POST http://localhost:8000/api/pagamentos/criar/ \
  -H "Content-Type: application/json" \
  -d '{"solicitacao": 13}'

# 3. depois de pagar, confirma (use o payment_id da URL de retorno)
curl -X POST http://localhost:8000/api/pagamentos/confirmar/ \
  -H "Content-Type: application/json" \
  -d '{"payment_id": "123456789"}'
```

**Regras do ambiente de teste do Mercado Pago**

- O vendedor de teste só recebe de **comprador de teste**. Entrar com a conta real faz o checkout recusar o pagamento.
- Use sempre janela anônima para não misturar com a sua conta real.
- Pague apenas com os cartões de teste.

---

### 11. Pendências e próximos passos

- **Webhook.** Hoje o pedido só é confirmado se o cliente voltar ao site. Se ele pagar e fechar a aba, o pedido fica em `AGP`. O webhook fará o Mercado Pago avisar o backend sozinho. Como `conciliar_pagamento` já é idempotente, o endpoint só precisa validar a assinatura (`x-signature`, com `MERCADOPAGO_WEBHOOK_SECRET`) e chamá-la. Exige o backend publicado em URL HTTPS pública, cadastrada no painel do Mercado Pago.
- **Pedidos abandonados.** Cada clique em "Ir para o pagamento" cria um pedido. Se o cliente desistir, ele fica em `AGP`. Vale criar uma rotina que cancele pedidos em `AGP` mais antigos que um certo prazo.
- **Estoque.** Não há controle de estoque no fluxo de pagamento.
- **Limite de requisições.** Os endpoints públicos (`/checkout/`, `/pagamentos/*`) não têm limitação de taxa. Considere usar *throttling* do DRF antes de produção.
- **Produção.** Gerar credenciais de **produção** novas, configurá-las apenas no painel da Vercel, e trocar `FRONTEND_URL` para a URL pública. As credenciais de teste usadas durante o desenvolvimento devem ser consideradas descartáveis.
- **Ambiente de desenvolvimento com IPv6.** Se `runserver` parecer travar ao conectar no banco (Neon), a rede pode estar tentando IPv6. Preferir IPv4 resolve (`precedence ::ffff:0:0/96 100` em `/etc/gai.conf`).

---

### 12. Problemas comuns

| Sintoma | Causa provável |
|---|---|
| `NameError` ao importar views | Import faltando (`generics`, `CheckoutSerializer`) ou view no arquivo errado |
| Servidor sobe e a porta não responde | Erro de import derrubou a thread, ou conexão com o banco travada |
| 400 em `/checkout/` | Campo ausente ou produto inexistente: a resposta indica qual |
| 400 em `/pagamentos/criar/` | Pedido não está em `AGP` |
| 502 em `/pagamentos/criar/` | Mercado Pago recusou; veja o log do backend |
| Checkout do MP recusa o pagamento "por ser conta de teste" | Logado na conta real, ou pagando com algo que não é cartão de teste |
| Volta ao site em página em branco | Rota do router diferente da `back_url` |
| Aprovado no MP, mas pedido segue `AGP` | `/pagamentos/confirmar/` não foi chamado ou falhou; veja o log |
| Erro de import `@/composables/usePagamento` | Arquivo fora de `src/composables/` ou com nome diferente (Linux diferencia maiúsculas) |
| Erro de tipo no `vue-tsc` | Tipo da função não bate com o que ela envia ou recebe |

---

### 13. Glossário rápido

| Termo | Significado |
|---|---|
| **Preferência** | O "carrinho" criado no Mercado Pago que gera o link de pagamento |
| **`init_point`** | URL da página de pagamento do Mercado Pago |
| **`external_reference`** | Nosso id de pedido, guardado no Mercado Pago e devolvido por ele |
| **Conciliação** | Fazer o nosso banco refletir o que o Mercado Pago diz |
| **Idempotência** | Repetir a operação não muda o resultado nem duplica nada |
| **Webhook** | O Mercado Pago chamando o nosso backend para avisar de um pagamento |
| **Composable** | Função do Vue que agrupa estado e lógica reutilizáveis |
| **Serializer** | Valida a entrada e formata a saída da API |
| **Service** | Camada que concentra a lógica de negócio ou de integração externa |