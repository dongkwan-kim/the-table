import csv
import datetime
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from session.models import UserProfile, UserPostProfile, BinaryQuestion
from prompt_responses.models import Response


class Command(BaseCommand):

    TYPE = [
        'profile',
        'response_explicit',
        'response_implicit',
    ]

    def add_arguments(self, parser):
        parser.add_argument('--type', help='file name')

    def handle(self, *args, **options):

        _type = options['type']
        file_name = "{0}_{1}.csv".format(_type,
                                         str(datetime.datetime.now()).replace(":", ""))
        if _type == 'profile':
            self.handle_profile(file_name)
        elif _type == 'response_explicit':
            self.handle_response(file_name, True)
        elif _type == 'response_implicit':
            self.handle_response(file_name, False)
        else:
            print("wrong type, use {0}".format(self.TYPE))

    def handle_response(self, file_name, user_answer_only):

        fields = ['id', 'user_id', 'object_id']

        r_ex = Response.objects.all()[0]
        text = json.loads(r_ex.text)
        fields += [k for k in text.keys()
                   if k not in ['demographics', 'answers']]

        p_ex = UserProfile.objects.all()[0]
        persona_field = [k for k in p_ex.get_persona_dict().keys()
                         if k not in ['completed', 'answers']]

        qnum_end = BinaryQuestion.objects.count() + 1
        persona_field += ['answers_{0}'.format(i) for i in range(1, qnum_end)]

        fields += persona_field

        wtr = writer_csv(file_name, fields)
        for r in Response.objects.all():

            profile = UserProfile.objects.get(user=r.user)

            d = {}
            d.update(r.__dict__)

            text = json.loads(r.text)
            d.update(dict([(k, v[0]) for (k, v) in text.items()
                           if k not in ['demographics', 'answers']]))

            user_persona = text['demographics'] + text['answers']
            p = {}
            if user_answer_only:
                for pf in persona_field:
                    if pf in user_persona:
                        p[pf] = profile.get_key(pf)
                    elif pf.startswith('answers_'):
                        n = pf.split("_")[1]
                        if n in user_persona:
                            answers = profile.get_key('answers')
                            p[pf] = answers[int(n) - 1]
                    if pf not in p:
                        p[pf] = False
            else:
                for pf in persona_field:
                    if pf.startswith('answers_'):
                        n = pf.split("_")[1]
                        answers = profile.get_key('answers')
                        p[pf] = answers[int(n) - 1]
                    else:
                        p[pf] = profile.get_key(pf)

            d.update(p)

            d = [(k, v) for (k, v) in d.items() if k in fields]
            wtr.writerow(dict(d))

    def handle_profile(self, file_name):

        fields = ['user_id']
        p_ex = UserProfile.objects.all()[0]
        fields += list(p_ex.get_persona_dict().keys())
        fields.remove('answers')
        qnum_end = BinaryQuestion.objects.count() + 1
        fields += ['answers_{0}'.format(i) for i in range(1, qnum_end)]
        fields += ['q{0}'.format(i) for i in range(1, 5)]

        wtr = writer_csv(file_name, fields)

        for user in User.objects.all():
            d = {}
            try:
                profile = UserProfile.objects.get(user=user)
                d.update(profile.__dict__)
                post_profile = UserPostProfile.objects.get(user=user)
                d.update(post_profile.__dict__)
            except:
                print("Error in ", user)
                continue

            answers = d['answers'].split(",")
            d = [(k, v) for (k, v) in d.items() if k in fields]
            d += [('answers_{0}'.format(i), answers[i - 1]) for i in range(1, qnum_end)]
            wtr.writerow(dict(d))


def writer_csv(filename: str, fieldnames: list):
    f = open(filename, "w", encoding="utf-8")
    wtr = csv.DictWriter(f, fieldnames=fieldnames)
    wtr.writeheader()
    return wtr

