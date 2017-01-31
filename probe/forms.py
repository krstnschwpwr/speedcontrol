from django import forms


class SettingsForm(forms.Form):
    expected_upload = forms.IntegerField(required=True)
    expected_download = forms.IntegerField(required=True)
    prtg_url = forms.CharField(required=False)
    prtg_token = forms.CharField(required=False)


