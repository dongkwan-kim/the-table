from django import forms
from session.models import UserProfile, BinaryQuestion
from prompt_responses.models import Prompt


class UserResponseForm(forms.Form):

    def __init__(self, request):

        super(UserResponseForm, self).__init__()

        self.request = request
        self.profile = UserProfile.objects.get(user=request.user)
        self.fields['demographics'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=self.get_demographics(),
        )
        self.fields['answers'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=self.get_binary_questions(),
        )

    def get_demographics(self):
        fields = [(f.verbose_name, f.name, self.profile.get_value(f.name)) \
                    for f in UserProfile._meta.fields \
                    if f.name not in ['id', 'user', 'answers']]
        return [(n, vn + ": " + v) for (vn, n, v) in fields]

    def get_binary_questions(self):
        fields = self.profile.get_value('answers')
        return fields


