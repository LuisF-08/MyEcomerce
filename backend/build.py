# backend/build.py
import os
import subprocess
import sys

# Executa o collectstatic automaticamente no momento da inicialização na Vercel
try:
    print("Executando collectstatic...")
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput", "--clear"], check=True)
except Exception as e:
    print(f"Erro ao rodar collectstatic: {e}")

# Importa a aplicação WSGI
from backend.wsgi import app