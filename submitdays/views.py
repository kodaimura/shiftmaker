from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm


def submitdays(request):
	obj = request.user.profile
	profile_form = ProfileForm(request.POST or None, instance=obj)

	if request.method == 'POST' and profile_form.is_valid():
		profile_form.save()
		return redirect('../mypage')

	context = {
		"loginuser": request.user,
		"profile_form": profile_form,
	}

	return render(request, 'submitdays/submitdays.html', context)
