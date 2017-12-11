from django import forms
from session.models import UserProfile, BinaryQuestion, UserPostProfile


class UserSignupForm(forms.Form):
    user_id = forms.CharField(label='아이디')
    password = forms.CharField(widget=forms.PasswordInput(), label='패스워드')

    def header(self):
        return '먼저, 계정을 생성해주세요'

    def btext(self):
        return '다음'


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user', 'answers', 'completed']

    def header(self):
        return '자신에 대해 조금 더 자세히 알려주세요'

    def btext(self):
        return '다음'


class UserPostProfileForm(forms.ModelForm):

    class Meta:
        model = UserPostProfile
        fields = '__all__'
        exclude = ['user']
        widgets ={
            'q1': forms.RadioSelect(),
            'q2': forms.RadioSelect(),
            'q3': forms.RadioSelect(),
            'q4': forms.RadioSelect(),
        }

    def header(self):
        return '주어진 문장에 대해 자신의 생각을 선택해주세요'

    def btext(self):
        return '제출'


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
        return '두 문장 중 어느 쪽이 당신의 생각과 가까운가요?'

    def btext(self):
        return '다음'


class ConsentForm(forms.Form):

    def __init__(self):

        super(ConsentForm, self).__init__()

        consent_href = "https://drive.google.com/file/d/1dvI7f4speZJulb823hDwmuxk81hfRgZW/view"
        consent_text = '<a target="_blank" href="{0}">인간대상연구동의서</a>'.format(consent_href) +\
                       '를 읽고 동의하신 후에 계정을 생성할 수 있습니다.'
        self.fields['consent'] = forms.ChoiceField(
            required=True,
            widget=forms.RadioSelect(),
            help_text=consent_text,
            choices=[(0, '인간대상연구동의서를 읽었고, 이에 동의합니다.')]
        )

    def header(self):
        return '인간대상연구동의'

    def btext(self):
        return '완료'
