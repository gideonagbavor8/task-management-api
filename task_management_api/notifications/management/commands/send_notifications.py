from django.core.management.base import BaseCommand
from tasks.utils import send_due_soon_notifications

class Command(BaseCommand):
    help = 'Send notifications for tasks due soon'

    def handle(self, *args, **kwargs):
        send_due_soon_notifications()
        self.stdout.write("Notifications sent successfully.")