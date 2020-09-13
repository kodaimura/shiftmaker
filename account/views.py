from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreateForm, LoginForm
from submitdays.forms import ProfileForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'account/login.html'


def signup(request):
    user_form = UserCreateForm(request.POST)
    profile_form = ProfileForm(request.POST)  
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():

    	user = user_form.save(commit=False)
    	user.is_active = True
    	user.save()

    	#userとprofileを紐付け -> user.profileでユーザの情報を参照可能に
    	profile = profile_form.save(commit=False)
    	profile.user = user
    	profile.save()
    	return redirect('../login/')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, 'account/signup.html', context)



