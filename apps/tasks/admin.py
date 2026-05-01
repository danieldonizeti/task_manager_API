from django.contrib import admin
from .models import Task, Category


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'category', 'user_id', 'created_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description')
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


