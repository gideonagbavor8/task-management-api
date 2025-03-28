from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Task

def send_due_soon_notifications():
    # Get tasks due within the next 24 hours
    due_soon = Task.objects.filter(
        due_date__lte=now() + timedelta(hours=24),
        status='Pending'
    )

    for task in due_soon:
        # Send an email to the task owner
        send_mail(
            subject=f"Reminder: Task '{task.title}' is due soon",
            message=f"Hello {task.user.username},\n\nYour task '{task.title}' is due on {task.due_date}. Please make sure to complete it on time.",
            from_email='gideonagbavor8@gmail.com',
            recipient_list=[task.user.email],
        )