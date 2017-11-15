from django import forms
from session.models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('user_id', 'password', 'age', 'gender', 'income', 'education',
                'occupation', 'political_affinity')
    user_id = forms.CharField(label='아이디')
    password = forms.CharField(widget=forms.PasswordInput(), label='패스워드')

