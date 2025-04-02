from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority_level', 'status', 'due_date', 'completed_timestamp')
    list_filter = ('priority_level', 'status', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('due_date',)  # Orders tasks by due date
    date_hierarchy = 'due_date'  # Adds a date-based drill-down navigation
