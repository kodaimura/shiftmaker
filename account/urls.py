from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
	path('', views.index),
	path('login/', views.Login.as_view()),
	path('logout/', views.Logout.as_view()),
	path('signup/', views.signup),
]