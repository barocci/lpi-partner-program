from django import forms

class AvatarForm(forms.Form):
    avatar = forms.ImageField(
        label='Select an avatar'
    )

    contact_id = forms.IntegerField()