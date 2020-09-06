from django import forms
from src.models import UnsubscribeEmail


class UnsubscribeForm(forms.ModelForm):
    class Meta:
        model = UnsubscribeEmail
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control w-50'})
