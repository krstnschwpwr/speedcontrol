from django import forms


class SettingsForm(forms.Form):
    upload = forms.IntegerField()
    download = forms.IntegerField()

