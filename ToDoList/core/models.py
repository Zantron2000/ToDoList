from django.db import models
from django.contrib.auth.models import User
import random, datetime

def generate_code():
    valid_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    code = ""

    for i in range(6):
        code += random.choice(valid_characters)

    return code

# Create your models here.
class TaskList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Task(models.Model):
    task = models.CharField(max_length=500)
    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.task
class UserValidation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6, default=generate_code)
    sent = models.BooleanField(default=False)

    def expired(self, minutes):
        time = self.date + datetime.timedelta(minutes=minutes)

        if(time < datetime.datetime.now(datetime.timezone.utc)):
            return True
        else:
            return False
    
    def generate_new_code(self):
        self.sent = False
        self.date = datetime.datetime.now(datetime.timezone.utc)
        self.code = generate_code()
        self.save()
    
