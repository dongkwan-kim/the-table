from django.contrib import admin
from grapp.models import Promise, Candidate, UserResponse, Election

def list_display_all(cls):
    return [x.name for x in cls._meta.fields if x.name != 'id']


@admin.register(Promise)
class PromiseAdmin(admin.ModelAdmin):
    list_display = list_display_all(Promise)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = list_display_all(Candidate)


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = list_display_all(UserResponse)


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = list_display_all(Election)


