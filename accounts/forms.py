from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control bg-light border-start-0 rounded-end-4',
                'placeholder': field.label
            })
        self.fields["email"].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.ROLE_STANDARD
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control bg-light border-start-0 rounded-end-4',
                'placeholder': field.label
            })
