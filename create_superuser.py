import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

try:
    if not User.objects.filter(username='ghoufrane').exists():
        User.objects.create_superuser('ghoufrane', 'ghoufranedaikra01@gmail.com', 'drip2026!')
        print('Superuser created!')
except Exception as e:
    print(f'Error: {e}')