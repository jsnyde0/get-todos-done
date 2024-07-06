from django.urls import include, path

app_name = "profiles"

urlpatterns = [
    path('', include('allauth.urls')),
]