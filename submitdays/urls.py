from django.urls import path
from . import views

app_name = 'submitdays'

urlpatterns = [
	path('submitdays', views.submitdays),
]