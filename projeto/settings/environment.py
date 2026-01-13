from pathlib import Path
import os
from utils.enviroment import get_env_variable, parse_comma_str_to_list

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('APP_SECRET_KEY','INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('APP_DEBUG') == 'S' else False

ALLOWED_HOSTS:list[str] = parse_comma_str_to_list(get_env_variable('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS:list[str] = parse_comma_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS'))

ROOT_URLCONF = 'projeto.urls'

WSGI_APPLICATION = 'projeto.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'