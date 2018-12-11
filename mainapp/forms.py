from django import forms


class FitCreationForm(forms.Form):
    fit_name = forms.CharField(max_length=200)
    fit_text = forms.CharField(max_length=4000, widget=forms.Textarea)
