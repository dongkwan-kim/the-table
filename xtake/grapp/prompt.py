from prompt_responses.models import Prompt
from grapp.models import Promise
from grapp.forms import UserResponseForm

import json


def get_prompt_ctx(request, shown_promise):
    response_prompt = Prompt.objects.get(id=1)
    response_prompt_form = UserResponseForm(request, shown_promise)

    return {
        'response_prompt_form': response_prompt_form,
        'response_prompt': response_prompt,
    }


def save_user_response(request):
    selected_promise_id = request.POST.get('selected_promise')
    selected_promise = Promise.objects.get(id=selected_promise_id)

    response_prompt = Prompt.objects.get(id=1)
    response_json = dict([(k, request.POST.getlist(k))
                          for k in UserResponseForm.get_fields()])

    response_prompt.create_response(
        user=request.user,
        prompt_object=selected_promise,
        text=json.dumps(response_json),
        rating=request.POST.get('stake'),
    )
