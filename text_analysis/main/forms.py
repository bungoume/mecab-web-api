from django import forms


class ReadingForm(forms.Form):
    sentence = forms.CharField(required=False)

    def clean_sentence(self):
        return self.cleaned_data.get('sentence', '')


class ParseForm(forms.Form):
    sentence = forms.CharField(required=False)

    def clean_sentence(self):
        return self.cleaned_data.get('sentence', '')
