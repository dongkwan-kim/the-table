from django.contrib import admin
from session.models import UserProfile, BinaryQuestion


def list_display_all(cls):
    return [x.name for x in cls._meta.fields if x.name != 'id']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = list_display_all(UserProfile)


@admin.register(BinaryQuestion)
class BinaryQuestionAdmin(admin.ModelAdmin):
    list_display = list_display_all(BinaryQuestion)

