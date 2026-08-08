# Instalação e execução

## Requisitos

| Componente | Versão mínima |
|------------|---------------|
| Python | 3.11+ |
| Node.js | 22.18+ ou 24.12+ |
| npm | compatível com Node |
| Redis | 7 (via Docker ou instalação local) |

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd MyEcomerce
```

## 2. Redis

```bash
cd docker
docker compose up -d
```

Redis ficará disponível em `127.0.0.1:6379`. O backend usa o banco `1` para cache.

## 3. Backend

### Ambiente virtual

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
```

### Dependências

```bash
pip install -r requirements.txt
```

O arquivo `backend/requirements.txt` lista as dependências do projeto. O `requirements.txt` na raiz do repositório é um dump do sistema operacional e deve ser ignorado.

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (lido por `backend/backend/settings.py`):

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Gere uma `SECRET_KEY` segura:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Banco de dados

```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

O superusuário criado deve ter `is_staff=True` (padrão do `createsuperuser`) para acessar o painel.

### Executar

```bash
python manage.py runserver
```

API: `http://localhost:8000`  
Swagger: `http://localhost:8000/api/docs/`

## 4. Frontend

```bash
cd frontend
npm install
```

Opcional — criar `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

### Executar

```bash
npm run dev
```

Aplicação: `http://localhost:5173`

### Build de produção

```bash
npm run build
npm run preview
```

## 5. Primeiro acesso

1. Acesse `http://localhost:5173/login` com o superusuário criado.
2. Configure a loja em `/admin/loja`.
3. Cadastre categorias e produtos.
4. Acesse a vitrine em `http://localhost:5173`.

## Comandos úteis

```bash
# Backend — shell Django
python manage.py shell

# Backend — popular dados de teste (stub)
python manage.py seed

# Backend — popular dashboard (comando customizado)
python manage.py popular_dashboard

# Frontend — lint
npm run lint

# Frontend — type-check
npm run type-check
```

## Estrutura de mídia

Uploads ficam em `backend/media/`:

```
media/
├── loja/logos/
├── loja/banner/
├── loja/produtos/
└── categorias/
```

Faça backup desta pasta junto com `db.sqlite3`.

## Problemas comuns

| Problema | Solução |
|----------|---------|
| Erro de CORS | Verifique se o frontend roda em `localhost:5173` ou adicione a origem em `CORS_ALLOWED_ORIGINS` |
| 401 no painel | Confirme que o usuário é staff; faça logout e login novamente |
| Cache não funciona | Verifique se o Redis está rodando na porta 6379 |
| Imagens não aparecem | Confirme `DEBUG=True` ou configure servidor de mídia em produção |
| SECRET_KEY ausente | Crie o arquivo `.env` na raiz com a variável configurada |

## Produção (orientações)

- Defina `DEBUG=False`
- Use PostgreSQL alterando `DATABASES` em `settings.py`
- Sirva mídia via nginx ou S3
- Configure HTTPS
- Use `gunicorn` ou similar como servidor WSGI
- Build estático do frontend (`npm run build`) servido pelo nginx ou CDN
