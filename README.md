# MyEcomerce

Plataforma de catálogo digital para pequenos comerciantes. O cliente navega pelos produtos, monta um carrinho e envia a solicitação pelo WhatsApp. O lojista gerencia produtos, categorias, pedidos e aparência da loja em um painel administrativo.

O sistema **não processa pagamentos**, **não calcula frete** e **não exige cadastro do cliente**.

## Stack

| Camada    | Tecnologias |
|-----------|-------------|
| Backend   | Python, Django 6, Django REST Framework, JWT, SQLite, Redis (cache) |
| Frontend  | Vue 3, TypeScript, Vite, Pinia, Tailwind CSS, PrimeVue, Chart.js |
| API       | REST, Swagger (`/api/docs/`) |

## Estrutura do repositório

```
MyEcomerce/
├── backend/          # API Django
│   ├── api/          # Views, serializers, permissions, services
│   ├── catalogo/     # Categorias e produtos
│   ├── loja/         # Configurações da loja
│   ├── solicitacao/  # Pedidos e itens
│   └── backend/      # Settings, URLs, WSGI
├── frontend/         # SPA Vue
├── docker/           # docker-compose (Redis)
└── docs/             # Documentação do projeto
```

## Início rápido

Consulte [docs/instalacao.md](docs/instalacao.md) para configurar backend, frontend e Redis.

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # configure SECRET_KEY e demais variáveis
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend (outro terminal)
cd frontend
npm install
npm run dev
```

- Loja pública: `http://localhost:5173`
- Painel admin: `http://localhost:5173/login`
- API Swagger: `http://localhost:8000/api/docs/`

## Documentação

| Documento | Conteúdo |
|-----------|----------|
| [docs/visao-geral.md](docs/visao-geral.md) | Objetivo, escopo e fluxos |
| [docs/arquitetura.md](docs/arquitetura.md) | Estrutura técnica e decisões |
| [docs/entidades.md](docs/entidades.md) | Modelo de dados |
| [docs/regras-negocio.md](docs/regras-negocio.md) | Regras e casos de uso |
| [docs/telas.md](docs/telas.md) | Telas do site e do painel |
| [docs/api.md](docs/api.md) | Endpoints e autenticação |
| [docs/instalacao.md](docs/instalacao.md) | Instalação e execução |
| [security.md](security.md) | Política de segurança |

## Funcionalidades

**Loja pública**
- Vitrine com banners, categorias e produtos em destaque
- Catálogo com busca, filtros e ordenação
- Carrinho persistido no `localStorage`
- Envio da solicitação via WhatsApp

**Painel administrativo**
- Login com JWT
- Dashboard com faturamento, pedidos e gráficos
- CRUD de produtos, categorias e configurações da loja
- Gestão de solicitações com controle de status
- Exportação de relatório CSV

## Autor

Luís Filipe Moreira Novais — Bacharelado em Sistemas de Informação, IFBA
