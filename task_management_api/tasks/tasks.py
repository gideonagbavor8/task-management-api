from celery import shared_task
from .utils import send_due_soon_notifications

@shared_task
def send_due_soon_notifications_task():
    send_due_soon_notifications()