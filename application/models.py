import datetime
import re

import cv2
from dateutil.utils import today
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django_quill.fields import QuillField
from django_undeletable.models import BaseModel, DataManager

from application.utils import NonStrippingTextField
from users.models import User
from webapp.storages import PrivateMediaStorage


class Device(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    browser = models.CharField(max_length=50)
    device = models.CharField(max_length=50)
    device_type = models.CharField(max_length=50)
    os = models.CharField(max_length=20)
    ip = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Gerät"
        verbose_name_plural = "Geräte"

    # method to fetch the ip of client
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    # Function for checking the browser, IP-address, and device info of the user
    def set_browser_info(self, request):
        # status of mobile, pc or tablet
        is_mobile = request.user_agent.is_mobile
        is_tablet = request.user_agent.is_tablet
        is_pc = request.user_agent.is_pc

        if is_mobile:
            self.device_type = "Mobile"
        elif is_tablet:
            self.device_type = "Tablet"
        elif is_pc:
            self.device_type = "PC or Laptop"
        else:
            self.device_type = "Unknown"

        # fetching the browser info
        browser_family = request.user_agent.browser.family
        self.browser = browser_family

        # fetching the os info
        os_family = request.user_agent.os.family
        self.os = os_family

        # fetching the device info
        device_name = request.user_agent.device.family
        self.device = device_name

        ip = self.get_client_ip(request)
        self.ip = ip

    def is_already_exists(self):
        device_queryset = Device.objects.filter(
            user=self.user,
            browser=self.browser,
            device=self.device,
            device_type=self.device_type,
            os=self.os,
            ip=self.ip,
        )

        return device_queryset.first()

    def is_limit_reached(self, limit=5):
        devices = Device.objects.filter(user=self.user)
        print(devices.count())
        return not devices.count() < limit

    def limit_is_nearly_reached(self, limit=3):
        devices = Device.objects.filter(user=self.user)
        print(devices.count())
        return not devices.count() < limit

    def save(self, *args, **kwargs):
        # figure out warranty end date
        if self.pk:
            self.last_login = timezone.now()
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user} - ({self.os}, {self.browser}, " f"{self.device_type}, {self.ip}, {self.session.session_key})"
        )


# signal to remove session from DB after deleting the device
@receiver(post_delete, sender=Device)
def delete_session(sender, instance, *args, **kwargs):
    instance.session.delete()


class Training(BaseModel):
    name = models.CharField(max_length=50)
    description = QuillField("Beschreibung", null=True, blank=True)
    thumbnail = models.ImageField(storage=PrivateMediaStorage(), verbose_name="Vorschaubild")
    modified = models.DateTimeField(auto_now=True, editable=False, null=True)
    ordering = models.IntegerField("Sortierung", default=0)

    hide_after_x_days = models.BooleanField("Nach 90 Tagen löschen", default=False)
    stick_to_the_plan = models.BooleanField("Reihenfolge einhalten", default=False)
    assign_after_days = models.IntegerField(
        help_text="Wird nach der eingestellten Anzahl an Tagen in der Mitgliedschaft automatisch freigegeben.",
        verbose_name="Automatisch freigeben",
        default=0,
    )  # used to grant access for users automatically after some time
    track_progress = models.BooleanField(default=False, verbose_name="Fortschritt zu Close übertragen")

    class Meta(BaseModel.Meta):
        verbose_name = "Kurs"
        verbose_name_plural = "Kurse"
        ordering = ["ordering"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("all_modules", args=[self.id])

    def get_all_modules(self):
        all_modules = Module.objects.filter(training=self)
        return all_modules

    def get_progress(self, completed_ids):
        completed = 0
        module_ids = Module.objects.filter(training=self).values_list("id", flat=True)
        all_medias = Media.objects.filter(module_id__in=module_ids).values_list("id", flat=True)
        for i in completed_ids:
            if i in all_medias:
                completed += 1

        media_count = all_medias.count()
        if media_count == 0:
            return 0
        return int((completed / media_count) * 100)

    def get_short_description(self):
        from html2text import html2text

        text = html2text(self.description.html, bodywidth=400)
        text = re.sub("\n\n", "\n", text)
        return text


class Module(BaseModel):
    name = models.CharField(max_length=50)
    description = NonStrippingTextField(verbose_name="Beschreibung")
    thumbnail = models.ImageField(storage=PrivateMediaStorage(), verbose_name="Vorschaubild")
    training = models.ForeignKey(Training, verbose_name="Kurs", on_delete=models.CASCADE)
    ordering = models.IntegerField("Sortierung", default=0)
    next = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="mod_next",
        null=True,
        blank=True,
        verbose_name="Nächstes",
    )

    modified = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Kapitel"
        verbose_name_plural = "Kapitel"
        ordering = ["ordering", "name"]

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("single_media", args=[self.module.training.id, self.module.id, self.id])

    def get_short_description(self):
        limit = 150
        description = self.description
        if len(description) > limit:
            return description[0:limit] + "..."
        return description

    def get_all_media_objects(self):
        return Media.objects.filter(module=self)

    def get_all_media(self):
        all_media = Media.objects.filter(module=self).values_list("name", flat=True)
        return all_media

    def get_progress(self, completed_ids):
        """used to get the progress for a different user"""
        completed = self.media_set.filter(id__in=completed_ids).count()
        if completed:
            return int(completed / self.media_set.count() * 100)
        return 0

    @cached_property
    def progress(self):
        if not hasattr(self, "completed_count"):
            raise Exception("progress darf hier nicht aufgerufen werden - es fehlt eine Annotation")
        if not self.completed_count:
            return 0
        return int((self.completed_count / self.media_set.count()) * 100)


class AttachmentStorage(FileSystemStorage):
    location = "media/attachments"

    def url(self, name):
        return "/media/attachments/" + name


class Media(BaseModel):
    name = models.CharField(max_length=50)
    description = NonStrippingTextField(verbose_name="Beschreibung")
    thumbnail = models.ImageField(storage=PrivateMediaStorage(), verbose_name="Vorschaubild")
    ordering = models.IntegerField("Sortierung", default=0)
    file = models.FileField(storage=PrivateMediaStorage(), verbose_name="Datei")
    length = models.CharField(verbose_name="Länge", max_length=50, default="", editable=False)
    module = models.ForeignKey(Module, verbose_name="Kapitel", on_delete=models.CASCADE)
    next = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="file_next",
        null=True,
        blank=True,
        verbose_name="Nächstes",
    )
    attachment = models.FileField(verbose_name="Anhang", null=True, storage=AttachmentStorage, blank=True)

    modified = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta(BaseModel.Meta):
        ordering = ["ordering", "name"]
        verbose_name = "Lektion"
        verbose_name_plural = "Lektionen"

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        # length must be saved after uploading the file since x3 will handle umlauts
        # and duplicated file names ..ergo the filename will likely change
        if not self.length:
            seconds = self.get_length()
            self.length = str(datetime.timedelta(seconds=seconds))
            self.save()

    def get_length(self):
        if self.get_file_type() == "audio":
            from mutagen.mp3 import MP3

            audio = MP3(self.file)
            length = audio.info.length
        else:
            data = cv2.VideoCapture(self.file.url)

            # count the number of frames
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(data.get(cv2.CAP_PROP_FPS))

            # calculate duration of the video
            length = int(frames / fps) if frames > 0 else 0
        return int(length)

    @cached_property
    def progress(self):
        if not hasattr(self, "is_completed"):
            raise Exception("Annotation fehlt!")
        if self.is_completed:
            return 100
        return 0

    def get_absolute_url(self):
        return reverse("single_media", args=[self.module.training.id, self.module.id, self.id])

    def get_file_type(self):
        file_name = self.file.name
        if file_name.endswith(".mp3") or file_name.endswith(".wav") or file_name.endswith(".wma"):
            return "audio"
        return "video"


class Access(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Nutzer")
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        verbose_name="Kurs",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Zugriff"
        verbose_name_plural = "Zugriffe"

    def __str__(self):
        return self.training.name


class Completed(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Nutzer")
    media = models.ForeignKey(Media, on_delete=models.CASCADE, verbose_name="Medien")

    class Meta(BaseModel.Meta):
        verbose_name = "Abgeschlossen"

    def __str__(self):
        return f"{self.media.name} ({self.media.id})"


class Page(BaseModel):
    url = models.CharField("URL", max_length=100, db_index=True)
    title = models.CharField("Titel", max_length=200)
    content = QuillField("Inhalt", null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Unterseite"
        verbose_name_plural = "Unterseiten"
        ordering = ["url"]

    def __str__(self):
        return self.title


class AppointmentManager(DataManager):
    def upcoming(self):
        date = today() + datetime.timedelta(days=90)
        return self.filter(date__gte=today(), date__lt=date)


class Appointment(BaseModel):
    name = models.CharField(max_length=100)
    date = models.DateField(verbose_name="Datum")
    start_time = models.TimeField(verbose_name="Startzeit")
    description = models.TextField(verbose_name="Beschreibung")
    link = models.URLField(verbose_name="Meeting-Link")

    data = AppointmentManager()

    class Meta(BaseModel.Meta):
        verbose_name = "Termin"
        verbose_name_plural = "Termine"
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.name } ({self.date})"


class Product(BaseModel):
    name = models.CharField(verbose_name="Name", max_length=100)
    courses = models.ManyToManyField(Training, verbose_name="Kurse")
    free = models.BooleanField("unbeschränkt", default=False)
    teaser = models.BooleanField(verbose_name="Beziehungs1x1", default=False)
    membership = models.BooleanField(verbose_name="Intensivzeit", default=False)

    can_view_zoom_link = models.BooleanField(verbose_name="Zoom-Link wird angezeigt", default=False)
    can_view_appointments = models.BooleanField(verbose_name="Termine werden angezeigt", default=False)
    can_view_forum = models.BooleanField(verbose_name="Forum wird angezeigt", default=False)

    class Meta(BaseModel.Meta):
        verbose_name = "Produkt"
        verbose_name_plural = "Produkte"

    def __str__(self):
        return self.name
