from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from grapp.step import *
from grapp.prompt import *


DEFAULT_RESULT = 'candidates'


def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')


@login_required()
def table(request, election, step):
    ctx = {}

    if request.method == "POST":
        save_user_response(request)
        main_cand_name = request.GET.get('main')
        next_path = './{0}?main={1}'.format(int(step) + 1, main_cand_name)
        return HttpResponseRedirect(next_path)

    else:
        if step == '0':
            ctx.update(get_choices_ctx(election))
            return render(request, 'choose.html', ctx)
        else:
            main_cand_name = request.GET.get('main')
            ctx.update(get_step_ctx(election, main_cand_name, step))
            if ctx['finished']:
                return HttpResponseRedirect('/result/{0}?kind={1}'.format(election, DEFAULT_RESULT))

            ctx.update(get_prompt_ctx(request, ctx['shown_promise']))
            return render(request, 'table.html', ctx)


def result(request, election):

    result_kind = request.GET.get('kind')
    template = 'result-{0}.html'.format(result_kind)
    ctx = get_result_ctx(request, election, result_kind)

    return render(request, template, ctx)
