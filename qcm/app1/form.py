from django import forms
from .models import CorrectAnswer


class CorrectAnswerForm(forms.ModelForm):
    class Meta:
        model = CorrectAnswer
        fields = ['question', 'answer']

    def __init__(self, *args, **kwargs):
        super(CorrectAnswerForm, self).__init__(*args, **kwargs)
