from django import forms

class AvatarForm(forms.Form):
    avatar = forms.ImageField(
        label='Select an avatar'
    )

    contact_id = forms.IntegerField()

class PasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)