from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

STATIC_ROOT  = BASE_DIR / 'staticfiles'
MEDIA_ROOT   = BASE_DIR / 'media'

# Use WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security headers
SECURE_BROWSER_XSS_FILTER    = True
SECURE_CONTENT_TYPE_NOSNIFF  = True
X_FRAME_OPTIONS              = 'DENY'

CELERY_TASK_ALWAYS_EAGER = False   # Use real Celery in production