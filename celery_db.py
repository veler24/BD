from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_kursach.settings')

# Создаем экземпляр Celery
app = Celery('django_kursach')

# Загружаем настройки из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в tasks.py всех приложений
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
