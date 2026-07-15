# Security Policy

## Visão Geral

O MyEcomerce utiliza boas práticas de segurança para proteger os dados da aplicação e restringir operações administrativas.

---

# Autenticação

A autenticação da API utiliza:

- JSON Web Token (JWT)

Endpoints:

```
POST /api/token/
POST /api/token/refresh/
```

---

# Permissões

### Público

- Visualizar produtos
- Visualizar categorias
- Enviar solicitações

### Administrador

- Gerenciar produtos
- Gerenciar categorias
- Gerenciar loja
- Dashboard
- Relatórios

---

# Validações

A API valida automaticamente:

- Campos obrigatórios
- Valores inválidos
- Estoque
- Preços
- Dados inconsistentes

---

# Proteção

- JWT
- Serializer Validation
- Permissions
- Django Admin protegido

---

# Boas práticas

- Nunca compartilhar a SECRET_KEY
- Utilizar HTTPS em produção
- Armazenar credenciais em variáveis de ambiente
- Atualizar dependências regularmente

---

# Reportar vulnerabilidades

Caso encontre alguma vulnerabilidade, entre em contato através do repositório do projeto.