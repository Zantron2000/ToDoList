from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from core.forms import NewUserForm, LoginForm, TaskForm
from . import models
from . import utils

# Create your views here.

@utils.logout_required(redirect_url="tasks")
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
                print("hello")
                login(request, user)
                
                return redirect("tasks")

    return render(request, "core/register.html", {"form": form})

@utils.logout_required(redirect_url="tasks")
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
@utils.group_required(group_name="Verified", redirect_url="verify")
def get_tasks(request: HttpRequest):

    user = request.user
    form = TaskForm()

    tasklisk:models.TaskList = models.TaskList.objects.get(user=user).task_set.all()
    
    return render(request, "core/tasks.html", {"tasklist": tasklisk, "form": form})

@login_required(login_url="login")
@utils.group_required(group_name="Verified", redirect_url="verify")
def create_task(request: HttpRequest):
    
    context = {"task":request.POST["task"], "tasklist":models.TaskList.objects.get(user=request.user)}
    newTask = models.Task(task=context["task"], tasklist=context["tasklist"])
    newTask.save()

    return redirect("tasks")

@login_required(login_url="login")
@utils.group_required(group_name="Verified", redirect_url="verify")
def delete_task(request: HttpRequest, pk: int):
    task:models.Task = models.Task.objects.get(id=pk)

    if(request.method == "POST"):
        task.delete()

    return redirect("tasks")

@login_required(login_url="login")
def logout_user(request: HttpRequest):
    logout(request)

    return redirect("login")

@login_required(login_url="login")
@utils.group_unrequired(group_name="Verified", redirect_url="tasks")
def verify_user(request: HttpRequest):
    valid:models.UserValidation = utils.get_validation(request.user)

    if(valid == None):
        valid = models.UserValidation(user=request.user)
        valid.save()
    elif(valid.expired()):
        valid.generate_new_code()
        
    if(request.method == "POST"):
        print(request.POST["code"])
        print(valid.code)
        if(request.POST["code"] == valid.code):
            group:Group = Group.objects.get(name="Verified")
            group.user_set.add(request.user)
            valid.delete()

            return redirect("tasks")

    if(valid.sent == False):
        sent = utils.send_email(request, valid)

        if(sent == 1):
            valid.sent = True
            valid.save()

    return render(request, "core/verify.html")

@login_required(login_url="login")
@utils.group_unrequired(group_name="Verified", redirect_url="tasks")
def test(request: HttpRequest):
    return HttpResponse("Done")