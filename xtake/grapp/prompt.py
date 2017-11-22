from prompt_responses.models import Prompt
from grapp.models import Promise
from grapp.forms import UserResponseForm


def get_prompt_ctx(request, shown_promise, selected_promise):

    prompt = Prompt.objects.get(id=1)
    form = UserResponseForm(request)

    return {
        'prompt_form': form,
        'prompt': prompt,
    }


