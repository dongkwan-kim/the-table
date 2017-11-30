from django import forms
from session.models import UserProfile, BinaryQuestion


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['user_id', 'password', 'age', 'gender', 'income', 'education',
                  'occupation', 'political_affinity']
    user_id = forms.CharField(label='아이디')
    password = forms.CharField(widget=forms.PasswordInput(), label='패스워드')

    def header(self):
        return '먼저, 계정을 생성해주세요'

    def btext(self):
        return '다음'


class QuestionForm(forms.Form):

    def __init__(self):

        super(QuestionForm, self).__init__()

        bq_list = BinaryQuestion.objects.all()

        for i, bq in enumerate(bq_list):
            name = 'q{0}'.format(str(i))
            self.fields[name] = self.add_choice(bq)

    def add_choice(self, bq):
        return forms.ChoiceField(
                choices=bq.get_choices(),
                help_text=("Q" + str(bq.num)),
                widget=forms.RadioSelect()
            )

    def header(self):
        return '두 문장 중 어느 쪽이 당신을 더 잘 설명하나요?'

    def btext(self):
        return '완료'
