from django import forms
from .models import Subscriber, Mailings


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['first_name', 'last_name', 'birth_date', 'email']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'name': 'birth_date'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'email': 'email'}),
        }


class MailingForm(forms.ModelForm):
    subscribers = forms.ModelMultipleChoiceField(
        queryset=Subscriber.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Подписчики'
    )

    class Meta:
        model = Mailings
        fields = ['subject', 'content', 'send_date', 'subscribers']
        widgets = {
            'send_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'name': 'send_date'}),
            'subject': forms.TextInput(
                attrs={'class': 'form-control', 'name': 'subject'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'name': 'content'}),
        }
