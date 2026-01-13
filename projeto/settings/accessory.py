from .environment import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

#Configurações de e-mail
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' #Simula o envio de e-mail

#Configuração de e-mail para ser usado em produção
DEFAULT_FROM_EMAIL = 'Fábio Rodrigues de Moraes'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'fmoraes05@gmail.com'
EMAIL_HOST_PASSWORD = 'xaejsornibdyacdu' #Essa senha é fornecida na configuração da sua conta Google criando o token em <senhas de app>
EMAIL_USER_TSL = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'

#OBS.: Feito a configuração acima, faça as configurações em views.py