from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
from copy import deepcopy
import json


class Election(models.Model):
    name = models.CharField(max_length=20)
    ko_name = models.CharField(max_length=20)
    year = models.IntegerField()
    help_description = models.TextField()
    game_step = models.IntegerField()

    def __str__(self):
        return self.ko_name


class Candidate(models.Model):
    name = models.CharField(max_length=10)
    party = models.CharField(max_length=10)
    election = models.ForeignKey(Election)
    region = models.CharField(max_length=20)
    profile = models.URLField()

    def __str__(self):
        return "-".join([self.name, self.party, self.region])

    def __lt__(self, other):
        return self.id < other.id


class Promise(models.Model):
    pid = models.IntegerField()
    candidate = models.ForeignKey(Candidate)
    title = models.TextField()
    description = models.TextField()
    related = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return "-".join([str(self.pid), self.title])

    def json(self):
        dcpy = deepcopy(self.__dict__)
        del dcpy['_state']
        return json.dumps(dcpy, ensure_ascii=False)
