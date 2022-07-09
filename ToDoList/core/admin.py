from django.contrib import admin

from core.models import Task, TaskList

# Register your models here.
admin.site.register(TaskList)
admin.site.register(Task)