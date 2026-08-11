import os
import sys
from django.core.wsgi import get_wsgi_application

# Obtém o caminho absoluto do diretório do projeto (a pasta pai de backend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
app = application