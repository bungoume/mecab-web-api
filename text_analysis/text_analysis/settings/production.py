from text_analysis.settings import *  # NOQA


ALLOWED_HOSTS = ['*']

DEBUG = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


#######################
# SECURITY MIDDLEWARE #
#######################
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
