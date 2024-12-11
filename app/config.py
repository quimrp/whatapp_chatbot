import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Función auxiliar para obtener variables de entorno requeridas
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"La variable de entorno {var_name} no está configurada")
    return value

# Database Configuration
DATABASE_URL = get_env_variable('DATABASE_URL')

# AWS Configuration
AWS_ACCESS_KEY = get_env_variable('AWS_ACCESS_KEY')
AWS_SECRET_KEY = get_env_variable('AWS_SECRET_KEY')
AWS_BUCKET_NAME = get_env_variable('AWS_BUCKET_NAME')

# AlvoChat Configuration
ALVOCHAT_TOKEN = get_env_variable('ALVOCHAT_TOKEN')
ALVOCHAT_INSTANCE_ID = get_env_variable('ALVOCHAT_INSTANCE_ID')
ALVOCHAT_API_URL = f"https://api.alvochat.com/{ALVOCHAT_INSTANCE_ID}"
ALVOCHAT_WEBHOOK_URL = get_env_variable('ALVOCHAT_WEBHOOK_URL')

# App Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Validación adicional
if not ALVOCHAT_API_URL.startswith("https://"):
    raise ValueError("ALVOCHAT_API_URL debe comenzar con 'https://'")

# Imprimir configuración (solo en modo debug)
if DEBUG:
    print("Configuración cargada:")
    print(f"DATABASE_URL: {DATABASE_URL}")
    print(f"AWS_BUCKET_NAME: {AWS_BUCKET_NAME}")
    print(f"ALVOCHAT_API_URL: {ALVOCHAT_API_URL}")
    print(f"ALVOCHAT_WEBHOOK_URL: {ALVOCHAT_WEBHOOK_URL}")
    print(f"DEBUG: {DEBUG}")

