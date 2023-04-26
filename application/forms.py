from django import forms
from django.forms import ModelForm

from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-Mail Adresse", required=True)
    password = forms.CharField(label="Passwort", widget=forms.PasswordInput, help_text=None)

    def is_user_exists(self, email):
        user = User.objects.filter(email=email)
        return user.first()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = self.is_user_exists(email)
        if user:
            if not user.check_password(password):
                self.add_error("password", "Falsches Passwort")
                return None
            return user
        else:
            self.add_error("email", "Diese Adresse ist nicht registriert")


class ForumNameForm(ModelForm):
    class Meta:
        model = User
        fields = ("forum_name",)

    @staticmethod
    def does_name_exist(name):
        user = User.data.filter(forum_name=name)
        return user.exists()

    def clean(self):
        cleaned_data = super().clean()
        forum_name = cleaned_data.get("forum_name")

        if self.does_name_exist(forum_name):
            self.add_error("forum_name", "Dieser Name ist nicht mehr verfügbar.")


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label="Passwort",
        max_length=20,
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        label="Passwort wiederholen", max_length=20, widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("password", "Passwörter stimmen nicht überein.")

        if password.isalpha() or password.isdigit():
            self.add_error("password", "Das Passwort muss Buchstaben und Zahlen enthalten.")

        if len(password) < 8:
            self.add_error("password", "Das Passwort muss mindestens 8 Zeichen enthalten.")
