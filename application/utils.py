from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import TextField


class NonStrippingTextField(TextField):
    """A TextField that does not strip whitespace at the beginning/end of
    it's value.  Might be important for markup/code."""

    def formfield(self, **kwargs):
        kwargs["strip"] = False
        return super(NonStrippingTextField, self).formfield(**kwargs)


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                ...

        if user and user.check_password(password):
            return user
