from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django_quill.fields import QuillField
from django_undeletable.models import BaseModel, UserDataManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        "Nutzername",
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # custom entries
    ############################################
    customer_number = models.CharField("Kundennummer", max_length=50, null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Die Telefonnummer muss in folgendem Format eingegeben werden: '+999999999'. Bis zu 15 Zeichen sind erlaubt.",
    )
    phone_number = models.CharField(
        "Telefonnummer", validators=[phone_regex], max_length=16, blank=True, null=True
    )
    street = models.CharField("Straße", max_length=255, blank=True, null=True)
    zip_code = models.CharField("PLZ", max_length=255, blank=True, null=True)
    city = models.CharField("Ort", max_length=255, blank=True, null=True)
    country = models.CharField("Land", max_length=255, blank=True, null=True)

    start_date = models.DateField("Start-Datum", blank=True, null=True)
    end_date = models.DateField("Ablauf-Datum", blank=True, null=True)

    zoom_link = models.URLField("Zoom-Link", blank=True, null=True)
    notes = QuillField("Notizen", null=True, blank=True)
    progress = models.FloatField(default=0)

    # PAARBOX
    paarbox_date = models.DateField(verbose_name="Datum", null=True, blank=True)
    paarbox_present = models.BooleanField(verbose_name="vorhanden", default=False)
    paarbox_sent = models.BooleanField(verbose_name="versendet", default=False)
    paarbox_handed_over = models.BooleanField(verbose_name="übergeben", default=False)

    # basic model stuff
    ############################################
    data = UserDataManager()
    objects = (
        UserDataManager()
    )  # this should stay due to compatibility issues with 3rd party libs

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta(BaseModel.Meta):
        verbose_name = "Nutzer"
        verbose_name_plural = "Nutzer"

    def clean(self):
        super(AbstractBaseUser, self).clean()
        self.email = self.__class__.data.normalize_email(self.email)

        test = self.paarbox_sent + self.paarbox_handed_over + self.paarbox_present
        if test > 1:
            raise ValidationError("Es kann nur eine Option ausgewählt werden! (Vorhanden, Übergeben oder Versendet)")

    def has_validity(self):
        return self.start_date and self.end_date

    def is_valid(self):
        return self.has_validity() and (self.start_date <= now().date() <= self.end_date)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def update_progress(self):
        from application.models import Media

        medias = Media.data.filter(module__training__in=self.access_set.values('training')).count()
        completed = self.completed_set.all().count()
        if medias and completed:
            ic(self, completed, medias)
            self.progress = completed / medias * 100
            self.save()

    # def email_user(
    #     self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs
    # ):
    #     """
    #      Sends an email to this User.
    #      If settings.EMAIL_OVERRIDE_ADDRESS is set, this mail will be redirected to the alternate mail address.
    #
    #     """
    #     receiver = self.email
    #     if settings.EMAIL_OVERRIDE_ADDRESS:
    #         receiver = settings.EMAIL_OVERRIDE_ADDRESS
    #
    #     send_mail(subject, message, from_email, [receiver], **kwargs)
