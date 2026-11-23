
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, ActivityRecord


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "This email is already being used."
            )

        return email


class ProfileDetailsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'contact_number',
        ]


        
class ActivityRecordForm(forms.ModelForm):

    class Meta:
        model = ActivityRecord
        fields = [
            'activity_name',
            'activity_type',
            'duration_minutes',
            'recorded_at',
            'notes',
        ]

        widgets = {
            'activity_name': forms.TextInput(attrs={
                'placeholder': 'Enter activity name'
            }),
            'recorded_at': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Optional notes'
            }),
        }

    def clean_activity_name(self):
        activity_name = self.cleaned_data.get('activity_name')

        if not activity_name or not activity_name.strip():
            raise forms.ValidationError(
                "Activity name cannot be empty."
            )

        return activity_name.strip()

    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')

        if duration is not None and duration < 1:
            raise forms.ValidationError(
                "Duration must be at least 1 minute."
            )

        return duration