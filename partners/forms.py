from django import forms

class AvatarForm(forms.Form):
    avatar = forms.ImageField(
        label='Select an avatar'
    )

    contact_id = forms.IntegerField()

class PasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)

class SubscriptionForm(forms.Form):
    id = forms.IntegerField(required=True)
    ref = forms.IntegerField(required=True)
    product = forms.CharField(required=True)

class AttachSubscriptionForm(forms.Form):
    company = forms.IntegerField(required=True)
    product = forms.CharField(required=True)



class WebhookForm(forms.Form):
    id = forms.IntegerField(required=True)
    event = forms.CharField(required=True)
    payload = forms.CharField(required=True)
