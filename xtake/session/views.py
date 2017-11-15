from django.shortcuts import render


def create_account(request):
    if request.method == "POST":
        # TODO w/ django forms
        raise NotImplementedError
    else:
        return render(request, 'persona.html')

