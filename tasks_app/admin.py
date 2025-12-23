from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'board', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'board')  # filtre pe lateral
    search_fields = ('title', 'description', 'board__title')
    filter_horizontal = ('assigned',)  # dacă e ManyToManyField