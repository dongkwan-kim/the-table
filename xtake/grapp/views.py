from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def table(request, election, step):
    user = request.user
    if user and user.is_authenticated():
        pass
    else:
        return HttpResponseRedirect('/account/basic/')

