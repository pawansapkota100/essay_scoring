from django import forms

from .models import Question, Essay
class AnswerForm(forms.ModelForm):
    answer = forms.CharField(max_length=100000, widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "What's on your mind?"}))

    class Meta:
        model = Essay
        fields = ['answer']

from grader.models import Profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'picture', 'location', 'date_of_birth', 'website', 'phone_number']
