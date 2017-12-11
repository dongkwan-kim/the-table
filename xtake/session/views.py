from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from session.forms import UserSignupForm, UserProfileForm, QuestionForm, ConsentForm, UserPostProfileForm
from session.models import UserProfile, BinaryQuestion


def create_account(request, step):

    is_signup = (step == 'signup')
    is_basic = (step == 'basic')
    is_question = (step == 'question')
    is_survey = (step == 'survey')

    if request.method == "POST":
        if is_survey:
            form = UserPostProfileForm(request.POST)
            if form.is_valid():
                post_profile = form.save(commit=False)
                post_profile.user = request.user
                post_profile.save()
            next_path = request.GET.get('next', '/')
            return HttpResponseRedirect(next_path)
        elif is_signup:
            user = User.objects.create_user(
                username=request.POST.get('user_id'),
                password=request.POST.get('password'),
            )
            user.save()
            login(request, user)
            return HttpResponseRedirect('/account/basic/')
        elif is_basic:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)

                # Delete exist one
                exist_profile = UserProfile.objects.filter(user=request.user)
                if exist_profile:
                    exist_profile[0].delete()

                profile.user = request.user
                profile.save()
            return HttpResponseRedirect('/account/question/')
        elif is_question:
            profile = UserProfile.objects.filter(user=request.user)[0]
            qnum = BinaryQuestion.objects.all().count()
            answers = [request.POST.get('q{0}'.format(i)) for i in range(qnum)]
            profile.set_answers(answers)
            profile.save()
            return HttpResponseRedirect('/account/consent/')
        else:
            profile = UserProfile.objects.filter(user=request.user)[0]
            consent = (request.POST.get('consent') == '0')
            profile.completed = consent
            profile.save()
            return HttpResponseRedirect('/table/pilot/0')
    else:
        if is_survey:
            form = UserPostProfileForm()
        elif is_signup:
            form = UserSignupForm()
        elif is_basic:
            form = UserProfileForm()
        elif is_question:
            form = QuestionForm()
        else:
            form = ConsentForm()

        ctx = {
            'form': form,
            'is_choice': not (is_signup or is_basic),
            'is_radio': is_survey,
            'header': form.header(),
            'btext': form.btext(),
        }
        return render(request, 'persona.html', ctx)
