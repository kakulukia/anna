from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext as _
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
    email = models.EmailField(_("email address"))
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
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Die Telefonnummer muss in folgendem Format eingegeben werden: '+999999999'. "
        "Bis zu 15 Zeichen sind erlaubt.",
    )
    phone_number = models.CharField(
        "Telefonnummer", validators=[phone_regex], max_length=16, blank=True, null=True
    )

    start_date = models.DateField("Start-Datum", blank=True, null=True)
    end_date = models.DateField("Ablauf-Datum", blank=True, null=True)
    bought_teaser = models.BooleanField(verbose_name="Beziehungs1x1", default=False)
    bought_membership = models.BooleanField(
        verbose_name="Akademie Beziehungskit", default=False
    )

    def active_member_default(self):
        if self.start_date and self.end_date:
            return self.start_date <= now().date() <= self.end_date
        return False

    active_member = models.BooleanField(
        verbose_name="Aktive Mitgliedschaft", null=False, blank=False, default=False
    )

    zoom_link = models.URLField("Zoom-Link", blank=True, null=True)
    progress = models.FloatField(default=0)
    forum_name = models.CharField(
        verbose_name="Forumname", max_length=40, null=True, blank=True
    )

    # CLOSE CMS STUFF - two contacts will share the same lead
    lead_id = models.CharField(max_length=70, null=True)
    contact_id = models.CharField(max_length=70, null=True, unique=True)

    # additional fields for SSO with Zulip
    ############################################
    @property
    def role(self):
        return 100 if self.is_superuser else 400

    # basic model stuff
    ############################################
    data = UserDataManager()
    objects = UserDataManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta(BaseModel.Meta):
        verbose_name = "Nutzer"
        verbose_name_plural = "Nutzer"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super(AbstractBaseUser, self).clean()
        self.email = self.__class__.data.normalize_email(self.email)

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

        medias = Media.data.filter(
            module__training__in=self.access_set.values("training")
        ).count()
        completed = self.completed_set.all().count()
        if medias and completed:
            self.progress = completed / medias * 100
            self.save()
        elif self.progress:
            self.progress = 0
            self.save()

    @property
    def customer_url(self):
        if not self.lead_id:
            return None

        url = f"https://app.close.com/lead/{self.lead_id}/"

        if self.contact_id:
            url += f"#contactId={self.contact_id}"

        return url

    @property
    def forum_url_helper(self):
        if self.forum_name:
            return "https://akademie.libendgern.de"
        else:
            return reverse("profile")

    # def email_user(
    #     self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL, **kwargs
    # ):
    #     """
    #      Sends an email to this User.
    #      If settings.EMAIL_OVERRIDE_ADDRESS is set, this mail will be redirected
    #      to the alternate mail address.
    #     """
    #     receiver = self.email
    #     if settings.EMAIL_OVERRIDE_ADDRESS:
    #         receiver = settings.EMAIL_OVERRIDE_ADDRESS
    #
    #     send_mail(subject, message, from_email, [receiver], **kwargs)
