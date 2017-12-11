from django import forms
from session.models import UserProfile, BinaryQuestion
from prompt_responses.models import Prompt


class UserResponseForm(forms.Form):

    def __init__(self, request, shown_promise):
        super(UserResponseForm, self).__init__()

        self.request = request
        self.profile = UserProfile.objects.get(user=request.user)

        self.fields['support'] = forms.ChoiceField(
            choices=self.get_supports(),
            help_text="이 공약을 지지하시나요?",
            widget=forms.RadioSelect()
        )
        self.fields['stake'] = forms.ChoiceField(
            choices=self.get_stakes(),
            help_text="이 공약을 지지하는지와는 상관없이,<br/> 이것이 현재의 당신에게 직접적으로 이익을 주나요, 손해를 주나요?",
            widget=forms.RadioSelect()
        )
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
        self.fields['open_ended'] = forms.CharField(
            required=False,
            help_text="선택지에 적당한 이유가 없다면, 이곳에 간단히 적어주세요",
            widget=forms.TextInput(),
        )
        self.fields['shown_promise'] = forms.CharField(
            initial=shown_promise.id,
            widget=forms.HiddenInput(),
        )
        self.fields['selected_promise'] = forms.CharField(
            initial=-1,
            widget=forms.HiddenInput(),
        )

    @classmethod
    def get_fields(cls):
        return ['support', 'stake', 'demographics', 'answers', 'open_ended', 'shown_promise', 'selected_promise']

    def get_supports(self):
        return [
            (0, "지지한다"),
            (1, "지지하지 않는다"),
            (2, "잘 모르겠다"),
        ]

    def get_stakes(self):
        return [(i, str(i)) for i in range(1, 6)]

    def get_demographics(self):
        fields = [(f.verbose_name, f.name, self.profile.get_value(f.name))
                  for f in UserProfile._meta.fields
                  if f.name not in ['id', 'user', 'answers', 'political_affinity', 'completed']]
        return [(n, vn + ": " + v) for (vn, n, v) in fields]

    def get_binary_questions(self):
        fields = self.profile.get_value('answers')
        return fields
