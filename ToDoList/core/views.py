from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

from core.forms import NewUserForm, LoginForm, TaskForm
from . import models

# Create your views here.
def register_user(request: HttpRequest):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if(form.is_valid()):
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])

            newList = models.TaskList(user=user)
            newList.save()

            if(user is not None):
                login(request, user)
                return redirect("tasks")

    return render(request, "core/register.html", {"form": form})

def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if(form.is_valid()):
            user = authenticate(username=form.username, password=form.password)
            if(user is not None):
                login(request, user)

                return redirect("tasks")

    return render(request, "core/login.html", {"form": form})

@login_required(login_url="login")
def get_tasks(request: HttpRequest):

    user = request.user
    form = TaskForm()

    tasklisk:models.TaskList = models.TaskList.objects.get(user=user).task_set.all()
    
    return render(request, "core/tasks.html", {"tasklist": tasklisk, "form": form})

@login_required
def create_task(request: HttpRequest):
    
    context = {"task":request.POST["task"], "tasklist":models.TaskList.objects.get(user=request.user)}
    newTask = models.Task(task=context["task"], tasklist=context["tasklist"])
    newTask.save()

    return redirect("tasks")

def delete_task(request: HttpRequest, pk: int):
    task:models.Task = models.Task.objects.get(id=pk)

    if(request.method == "POST"):
        task.delete()

    return redirect("tasks")