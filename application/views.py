import re
import uuid
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import logout, user_logged_in
from django.contrib.auth.decorators import login_required
from django.db.models import Count, OuterRef, Q, Subquery
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from application.forms import ForumNameForm, ResetPasswordForm
from application.models import (
    Access,
    Appointment,
    Completed,
    Device,
    Media,
    Module,
    Page,
    Training,
)
from users.models import User


# Signals to add device in logged in device
@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    request.session.save()
    session_id = request.session.session_key
    new_device = Device(user=user, session_id=session_id)
    new_device.set_browser_info(request)
    is_exists = new_device.is_already_exists()
    if is_exists:
        new_device = is_exists
        new_device.session_id = session_id

    else:
        if new_device.is_limit_reached():
            messages.error(request, "Du hast die maximale Anzahl an Geräten erreicht.")
            if not request.user.is_superuser:
                logout(request)
                return

        if new_device.limit_is_nearly_reached():
            messages.warning(
                request,
                mark_safe(
                    "Du hast bereits 4 Geräte angemeldet."
                    "Bitte lösche ein Gerät <a href='/profile/#devices'>hier >>></a>."
                ),
            )

    new_device.save()


@login_required
def reset_password(request):
    if request.method == "POST":
        password_form = ResetPasswordForm(request.POST)
        if password_form.is_valid():
            password = password_form.cleaned_data["password"]
            print(password)
            user = request.user
            user.set_password(password)
            user.save()
            messages.success(request, "Dein neues Passwort wurde gespeichert.")
        else:
            messages.error(request, password_form.errors)

    return redirect("profile")


@login_required
def profile(request):
    def get_initial_value():
        if request.user.forum_name:
            return request.user.forum_name

        name = request.user.get_full_name()

        while User.data.filter(forum_name=name).exists():
            name = name + "1"

        return name

    forum_name_form = ForumNameForm(instance=request.user, initial={"forum_name": get_initial_value()})
    password_form = ResetPasswordForm()

    if request.method == "POST":
        forum_name_form = ForumNameForm(request.POST, instance=request.user)
        if forum_name_form.is_valid():
            messages.success(request, "Das Profil wurde aktualisiert.")
            forum_name_form.save()

    device_sessions = Device.objects.filter(user=request.user)
    all_trainings = Access.objects.filter(user=request.user)

    completed_media_ids = Completed.data.filter(user=request.user).values_list("media_id", flat=True)

    for access in all_trainings:
        training = access.training
        training.progress = training.get_progress(completed_media_ids)

    context = {
        "all_trainings": all_trainings,
        "forum_name_form": forum_name_form,
        "page": "profile",
        "device_sessions": device_sessions,
        "password_form": password_form,
        "accessed_training": get_accessed_training(request.user),
    }
    return render(request, "profile.html", context)


@login_required
def index(request):
    return redirect("trainings")


# function for logout
def signout(request):
    logout(request)
    return redirect("login")


# Function for checking the browser, IP-address, and device info of the user
def get_browser_info(request):
    # status of mobile, pc or tablet
    is_mobile = request.user_agent.is_mobile
    is_tablet = request.user_agent.is_tablet
    is_pc = request.user_agent.is_pc

    # fetching the browser info
    browser_family = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version

    # fetching the os info
    os_family = request.user_agent.os.family
    os_version = request.user_agent.os.version

    # fetching the device info
    device_name = request.user_agent.device.family
    ip = Device.get_client_ip(request)

    test = ":".join(re.findall("..", "%012x" % uuid.getnode()))

    str = (
        f"The {request.user.last_name} is on the Mobile: {is_mobile}\n"
        f"The {request.user.last_name} is on the Tablet: {is_tablet}\n"
        f"The {request.user.last_name} is on the PC: {is_pc}\n"
        f"The {request.user.last_name} Browser is: {browser_family}\n"
        f"The {request.user.last_name} Browser Version is: {browser_version}\n"
        f"The {request.user.last_name} OS is: {os_family}\n"
        f"The {request.user.last_name} OS Version is: {os_version}\n"
        f"The {request.user.last_name} Device is: {device_name}\n\n{test}"
    )
    # print(test)
    # print(type(test))

    # joins elements of getnode() after each 2 digits.
    # using regex expression
    print("The MAC address in formatted and less complex way is : ", end="")
    print(":".join(re.findall("..", "%012x" % uuid.getnode())))

    print(ip)
    return HttpResponse(str)


@login_required
def delete_user_device(request, device_id):
    # filtering if the device with the given id exists or not
    # device = Device.objects.filter(id=device_id)
    device = get_object_or_404(Device, pk=device_id)

    if device.user == request.user:
        device.delete()
        return HttpResponseRedirect(reverse("profile"))
    else:
        return HttpResponseRedirect(reverse("profile"))


def get_accessed_training_objects(user):
    return Access.data.filter(user=user)


def get_accessed_training(user):
    access_objs = get_accessed_training_objects(user)
    return access_objs.values_list("training_id", flat=True)


@login_required
def all_trainings(request):
    trainings = Training.data.filter(access__in=Access.data.filter(user=request.user))
    accessed_training = get_accessed_training(request.user)

    expand_id = request.GET.get("expand")
    if expand_id:
        training = Training.objects.filter(id=expand_id).first()
    else:
        training = trainings.first()
    allowed = training and training.id in accessed_training
    completed_media_ids = Completed.data.filter(user=request.user).values_list("media_id", flat=True)

    for single_training in trainings:
        if single_training.id in accessed_training:
            single_training.progress = single_training.get_progress(completed_media_ids)

    context = {
        "allowed": allowed,
        "training": training,
        "trainings": trainings,
        "accessed_training": accessed_training,
    }
    return render(request, "all_trainings.html", context)


@login_required
def progress(request):
    if not request.user.is_superuser:
        messages.error(request, "Du hast keine Berechtigung für diese Seite.")
        return redirect("index")

    all_users = User.data.filter(is_superuser=False)
    search_text = ""
    if request.method == "POST" and "filter" in request.POST:
        search_text = request.POST["filter"]
        all_users = all_users.filter(Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text))
    updated_users = []
    for user in all_users:
        access_objects = get_accessed_training(user)
        updated_users.append({"user": user, "count": access_objects.count()})

    context = {"users": updated_users, "search_text": search_text}
    return render(request, "progress/index.html", context)


@login_required
def progress_trainings(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Du hast keine Berechtigung für diese Seite.")
        return redirect("index")

    all_users = User.objects.filter(is_superuser=False)[1:]
    current_user = User.objects.get(id=id)
    current_user_trainings = get_accessed_training_objects(current_user)
    completed_media_ids = Completed.data.filter(user=current_user).values_list("media_id", flat=True)
    current_user_trainings_updated = []
    for access in current_user_trainings:
        my_training = access.training
        my_training.progress = my_training.get_progress(completed_media_ids)
        current_user_trainings_updated.append(my_training)

    updated_users = []
    for user in all_users:
        access_objects = get_accessed_training(user)
        updated_users.append({"user": user, "count": access_objects.count()})

    context = {
        "trainings": current_user_trainings_updated,
        "users": updated_users,
        "current_user": current_user,
        # "search-text": search_text
    }
    return render(request, "progress/training_progress.html", context)


@login_required
def all_modules(request, training_id):
    training = Training.objects.get(id=training_id)

    if not Access.objects.filter(user=request.user, training=training).exists():
        messages.error(request, "Du hast keinen Zugriff auf diesen Kurs.")
        return redirect("trainings")

    modules = (
        Module.data.filter(training=training)
        .annotate(completed_count=Count("media__completed", filter=Q(media__completed__user=request.user)))
        .order_by("ordering")
    )
    context = {"training": training, "modules": modules}
    return render(request, "all_modules.html", context)


@login_required
def all_medias(request, training_id, module_id):
    training = get_object_or_404(Training, id=training_id)
    module = get_object_or_404(
        Module.data.all().annotate(
            completed_count=Count("media__completed", filter=Q(media__completed__user=request.user))
        ),
        id=module_id,
    )

    if not Access.objects.filter(user=request.user, training=training).exists():
        messages.error(request, "Du hast keinen Zugriff auf diesen Kurs.")
        return redirect("trainings")

    context = {"module": module}
    return render(request, "all_media.html", context)


@login_required
def progress_modules(request, id, training_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page")
        return redirect("index")

    all_users = User.objects.filter(is_superuser=False)
    current_user = User.objects.get(id=id)
    completed_media_ids = Completed.data.filter(user=current_user).values_list("media_id", flat=True)
    current_training = get_object_or_404(Training, id=training_id)
    current_training.progress = current_training.get_progress(completed_media_ids)
    updated_users = []
    for user in all_users:
        access_objects = get_accessed_training(user)
        updated_users.append({"user": user, "count": access_objects.count()})

    # Fetching modules
    modules = Module.objects.filter(training=current_training)
    for module in modules:
        module.user_progress = module.get_progress(completed_media_ids)

    # Fetching completed medias
    completed_media_ids = Completed.data.filter(user=current_user).values_list("media_id", flat=True)

    context = {
        "completed_media": completed_media_ids,
        "modules": modules,
        "training": current_training,
        "users": updated_users,
        "current_user": current_user,
    }
    return render(request, "progress/module_progress.html", context)


@login_required
def resume_all_modules(request, training_id):
    training = Training.objects.get(id=training_id)
    modules = Module.objects.filter(training=training)
    modules_ids = modules.values_list("id", flat=True)
    all_media_ids = Media.objects.filter(module_id__in=modules_ids).values_list("id", flat=True)
    completed_media_ids = Completed.data.filter(media_id__in=all_media_ids, user=request.user).values_list(
        "media_id", flat=True
    )
    # all media objects ids list
    all_media_ids_list = list(all_media_ids)
    # all compeleted objects ids list
    completed_media_ids_list = list(completed_media_ids)
    # if not
    redirected_media_id = get_remaining_media_id(all_media_ids_list, completed_media_ids_list)

    if len(completed_media_ids_list) == 0:
        return main_media(request, redirected_media_id)

    if len(all_media_ids_list) != len(completed_media_ids_list) and len(completed_media_ids_list) != 0:
        return main_media(request, redirected_media_id)

    for module in modules:
        module.progress = module.get_progress(completed_media_ids)
    context = {"training": training, "modules": modules}
    return render(request, "all_modules.html", context)


def main_media(request, media_id):
    media = Media.objects.filter(id=media_id).first()
    if not media:
        return redirect("trainings")

    module_id = media.module.id
    training_id = media.module.training.id
    return redirect("single_media", training_id=training_id, module_id=module_id, media_id=media_id)


def get_remaining_media_id(all_media_ids_list, completed_media_ids_list):
    for all_media_id in all_media_ids_list:
        if all_media_id in completed_media_ids_list:
            continue
        else:
            return all_media_id


@login_required
def media(request, training_id, module_id, media_id=None):
    module = Module.data.annotate(
        completed_count=Count("media__completed", filter=Q(media__completed__user=request.user))
    ).get(id=module_id)

    if not Access.objects.filter(user=request.user, training=module.training).exists():
        messages.error(request, "Du hast keinen Zugriff auf diesen Kurs.")
        return redirect("trainings")

    media_set = Media.data.filter(module=module).annotate(
        is_completed=Count("completed", filter=Q(completed__user=request.user))
    )
    # annotate the previous media if any for reference in the next step
    previous = Media.data.filter(next=OuterRef("pk")).values("id")[:1]
    media_set = media_set.annotate(previous=Subquery(previous))

    previous_completed = Completed.data.filter(media=OuterRef("previous"), user=request.user)
    media_set = media_set.annotate(previous_completed=Subquery(previous_completed.values("id")))

    # if the video is older than 90 days hide it
    if module.training.hide_after_x_days:
        today = datetime.now().date()
        refercens_day = today - timedelta(days=90)
        media_set = media_set.filter(created__gt=refercens_day)

    context = {
        "module": module,
        "media_set": media_set.order_by("ordering", "name"),
    }
    return render(request, "all_media.html", context)


@login_required
def mark_as_done(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    if not media:
        messages.error(request, "Invalid action")
        return redirect("trainings")

    training = media.module.training
    if not Access.objects.filter(user=request.user, training=training).exists():
        messages.error(request, "Du hast keinen Zugriff auf diesen Kurs.")
        return redirect("trainings")

    if not request.user.completed_set.filter(media=media).exists():
        Completed.data.create(user=request.user, media=media)
    request.user.update_progress()

    if media.next:
        media = media.next
        messages.success(request, "Lektion als abgeschlossen markiert")
        training_id = media.module.training.id
        module_id = media.module.id
        media_id = media.id
        return redirect("single_media", training_id=training_id, module_id=module_id, media_id=media_id)

    if media.module.next:
        messages.success(request, "Kapitel als abgeschlossen markiert")
        next_module = media.module.next
        training_id = next_module.training.id
        module_id = next_module.id
        return redirect("media", training_id=training_id, module_id=module_id)

    messages.success(request, "Kurs wurde abgeschlossen")
    return redirect("trainings")


# Function to render the single_media page


@login_required
def single_media(request, training_id, module_id, media_id):
    training = Training.objects.get(id=training_id)
    module = Module.objects.get(id=module_id)
    media = Media.objects.annotate(is_completed=Count("completed", filter=Q(completed__user=request.user))).get(
        id=media_id
    )
    medias = Media.objects.filter(module=module)
    context = {
        "module": module,
        "media": media,
        "training": training,
        "medias": medias,
    }
    template = "single_media_content.html" if "video-only" in request.GET else "single_media.html"
    return render(request, template, context)


def render_flatpage(request, url):
    page = get_object_or_404(Page, url=url)

    title = mark_safe(page.title)
    content = mark_safe(page.content.html)

    return render(request, "flatpage.html", {"title": title, "content": content})


@login_required
def appointments(request):
    context = {"appointments": Appointment.data.upcoming()}
    return render(request, "appointments.html", context)


@login_required
def forum(request):
    return render(request, "forum.html")


@login_required
def copy_media(request, media_id, module_id):
    old_media = get_object_or_404(Media, pk=media_id)
    module = get_object_or_404(Module, pk=module_id)

    new_media = old_media
    new_media.pk = None
    new_media.ordering = module.media_set.count()
    new_media.module = module
    new_media.next = None

    last_item = module.media_set.last()

    new_media.save()

    if last_item:
        last_item.next = new_media
        last_item.save()

    return HttpResponseRedirect(reverse("admin:application_media_change", args=[new_media.pk]))
