from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from session.forms import UserProfileForm, QuestionForm
from session.models import UserProfile, BinaryQuestion


def create_account(request, step):
    is_basic = (step == 'basic')
    if request.method == "POST":
        if is_basic:
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
            return HttpResponseRedirect('/account/question/')
        else:
            profile = UserProfile.objects.filter(user=request.user)[0]
            qnum = BinaryQuestion.objects.all().count()
            answers = [request.POST.get('q{0}'.format(i)) for i in range(qnum)]
            profile.set_answers(answers)
            profile.save()
            return HttpResponseRedirect('/table/pilot/0')
    else:
        if is_basic:
            form = UserProfileForm()
        else:
            form = QuestionForm()
        ctx = {
            'form': form,
            'is_basic': is_basic,
            'header': form.header(),
            'btext': form.btext(),
        }
        return render(request, 'persona.html', ctx)
