from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from grapp.step import *
from grapp.prompt import *


def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def table(request, election, step):
    user = request.user
    ctx = {}
    if user and user.is_authenticated():

        if step == '0':
            ctx.update(get_choices_ctx(election))
            return render(request, 'choose.html', ctx)
        else:
            main_cand_name = request.GET.get('main')
            ctx.update(get_step_ctx(election, main_cand_name, step))
            ctx.update(get_prompt_ctx(request, ctx['shown_promise'], ctx['selected_promises']))
            return render(request, 'table.html', ctx)
    else:
        return HttpResponseRedirect('/account/basic/')

