from prompt_responses.models import Prompt
from grapp.models import Promise
from grapp.forms import UserResponseForm

import json


def get_prompt_ctx(request, shown_promise, selected_promise):

    prompt = Prompt.objects.get(id=1)
    form = UserResponseForm(request)

    return {
        'prompt_form': form,
        'prompt': prompt,
    }


def save_user_response(request):

    prompt = Prompt.objects.get(id=1)
    res_json = dict([(k, request.POST.getlist(k)) for k in ['demographics', 'answers']])

    prompt.create_response(
        user=request.user,
        text= json.dumps(res_json),
    )

