from django.contrib import admin

from core.models import Task, TaskList, UserValidation

# Register your models here.
admin.site.register(TaskList)
admin.site.register(Task)
admin.site.register(UserValidation)