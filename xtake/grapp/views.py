from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from grapp.step import *


def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def table(request, election, step):
    user = request.user
    ctx = {}
    if user and user.is_authenticated():
        main_cand_name = request.GET.get('main')
        ctx.update(get_step_ctx(election, main_cand_name, step))
        return render(request, 'table.html', ctx)
    else:
        return HttpResponseRedirect('/account/basic/')

