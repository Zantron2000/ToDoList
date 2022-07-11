from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("tasklist", views.get_tasks, name="tasks"),
    path("create", views.create_task, name="create"),
    path("delete/<int:pk>", views.delete_task, name="delete"),
    path("logout", views.logout_user, name="logout")
]