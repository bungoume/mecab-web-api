from django import forms
from django.core import validators


class ReadingForm(forms.Form):
    sentence = forms.CharField(required=False)
    nbest_num = forms.IntegerField(validators=[
        validators.MinValueValidator(1), validators.MaxValueValidator(50)], required=False)

    def clean_sentence(self):
        return self.cleaned_data.get('sentence', '')

    def clean_nbest_num(self):
        nbest_num = self.cleaned_data.get('nbest_num')
        if nbest_num is None:
            return 10
        return nbest_num


class ParseForm(forms.Form):
    sentence = forms.CharField(required=False)
    nbest_num = forms.IntegerField(validators=[
        validators.MinValueValidator(1), validators.MaxValueValidator(50)], required=False)

    def clean_sentence(self):
        return self.cleaned_data.get('sentence', '')

    def clean_nbest_num(self):
        nbest_num = self.cleaned_data.get('nbest_num')
        if nbest_num is None:
            return 3
        return nbest_num
