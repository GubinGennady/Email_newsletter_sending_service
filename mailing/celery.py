# import os
#
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')
#
# app = Celery('mailing')
# app.conf.broker_connection_retry_on_startup = True
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')

# Автоперезапуск при ошибках соединения
app.conf.broker_connection_retry_on_startup = True

# Загружаем конфигурацию из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
