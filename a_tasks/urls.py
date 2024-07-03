"""
URL configuration for a_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

app_name = 'tasks'

urlpatterns = [
    path('', views.list_view, name='home'),
    # path('task/create/', views.create_task, name='create_task'),
    path('task/<str:id>/', views.view_update_task, name='view_task'),
    path('task/<str:id>/edit/', views.view_update_task, name='view_update_task'),
    path('task/<str:id>/complete/', views.toggle_task_completed, name='toggle_task_completed'),
]