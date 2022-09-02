import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings')

app = Celery('Artifact')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # 'update_every_5_minute': {
    #     'task': 'src.apps.posts.tasks.update',
    #     'schedule': crontab(minute='*/5'),
    # }
}
