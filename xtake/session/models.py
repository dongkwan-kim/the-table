from django.contrib.auth.models import User
from django.db import models


class BinaryQuestion(models.Model):
    num = models.IntegerField()
    choice_1 = models.TextField()
    choice_2 = models.TextField()


class UserProfile(models.Model):
    user = models.ForeignKey(User)

    """
    [1] 박찬욱. "한국인 정치참여의 특징과 결정요인: 2004 년 조사결과 분석." (2005).

    """
    age = models.IntegerField()
    gender = models.IntegerField()
    income = models.IntegerField()
    education = models.IntegerField()
    occupation = models.IntegerField()
    political_affinity = models.IntegerField()

    # csv
    answers = models.TextField()

    def __str__(self):
        return str(user)

    def get_answers(self):
        return [int(x) for x in self.answers.split(",")]

    def set_answers(self, lst):
        self.answers = ",".join([str(x) for x in lst])



