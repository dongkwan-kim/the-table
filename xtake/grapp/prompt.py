from prompt_responses.models import Prompt
from grapp.models import Promise
from grapp.forms import UserResponseForm

import json


def get_prompt_ctx(request, shown_promise):

    prompt = Prompt.objects.get(id=1)
    form = UserResponseForm(request, shown_promise)

    return {
        'prompt_form': form,
        'prompt': prompt,
    }


def save_user_response(request):

    prompt = Prompt.objects.get(id=1)
    selected_promise_id = request.POST.get('selected_promise')
    selected_promise = Promise.objects.get(id=selected_promise_id)
    res_json = dict([(k, request.POST.getlist(k)) \
                for k in ['demographics', 'answers', 'shown_promise']])

    prompt.create_response(
        user=request.user,
        prompt_object=selected_promise,
        text=json.dumps(res_json),
    )

