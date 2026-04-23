from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'user_id', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')


