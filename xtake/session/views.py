from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from session.forms import UserProfileForm


def create_account(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            user = User.objects.create_user(
                    username=request.POST.get('user_id'),
                    password=request.POST.get('password'),
                )
            user.save()
            profile.user = user
            profile.save()
            login(request, user)
        return HttpResponseRedirect('/table/pilot/0')
    else:
        form = UserProfileForm()
        return render(request, 'persona.html', {'form': form})


