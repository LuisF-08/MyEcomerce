# Política de segurança

## Escopo

Este documento descreve as medidas de segurança do MyEcomerce e como reportar vulnerabilidades.

## Autenticação

A API usa JSON Web Token (JWT) via `djangorestframework-simplejwt`.

| Endpoint | Função |
|----------|--------|
| `POST /api/token/` | Obter access + refresh token |
| `POST /api/token/refresh/` | Renovar access token |

Configuração atual:

- Access token: 30 minutos
- Refresh token: 7 dias, com rotação e blacklist após rotação
- Header: `Authorization: Bearer <token>`

O frontend armazena tokens em `localStorage`. Em produção com HTTPS, considere avaliar alternativas (httpOnly cookies) conforme o perfil de risco.

## Autorização

Permissão padrão da API: autenticado (`IsAuthenticated`). ViewSets aplicam exceções:

| Classe | Comportamento |
|--------|---------------|
| `AdminOuLeitura` | `list` e `retrieve` públicos; demais ações exigem `is_staff` |
| `AdminOuCria` | `create` público (solicitações); demais ações exigem admin |

Dashboard, exportação CSV e endpoints de escrita de produtos/categorias/loja exigem usuário staff.

## Validação de dados

- Serializers DRF validam campos obrigatórios, tipos e regras (ex.: quantidade mínima em itens de solicitação).
- Upload de imagens processado via Pillow.
- Senhas validadas pelos validators padrão do Django.

## Configuração sensível

Variáveis lidas de `.env` via `python-decouple`:

| Variável | Uso |
|----------|-----|
| `SECRET_KEY` | Assinatura de tokens e sessões Django |
| `DEBUG` | Modo debug (deve ser `False` em produção) |
| `ALLOWED_HOSTS` | Hosts permitidos |

**Nunca** commite `.env` ou chaves reais no repositório.

## CORS

Em desenvolvimento, apenas `http://localhost:5173` está autorizado. Restrinja origens em produção.

## Boas práticas

1. Use HTTPS em produção.
2. Mantenha `DEBUG=False` em produção.
3. Atualize dependências regularmente.
4. Crie superusuários com senhas fortes.
5. Faça backup de `db.sqlite3` e `media/`.
6. Não exponha `/api/docs/` publicamente em produção sem autenticação adicional, se desejado.

## Reportar vulnerabilidades

Se encontrar uma vulnerabilidade de segurança, abra uma issue privada ou entre em contato pelo repositório do projeto. Descreva:

- Passos para reproduzir
- Impacto estimado
- Versão/commit afetado

Não divulgue publicamente antes de correção, quando possível.
