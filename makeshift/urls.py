from django.urls import path
from . import views

app_name = 'makeshift'

urlpatterns = [
	path('', views.mypage),
	path('shift', views.shift),
	#path('keepshift', views.keepshift),
]