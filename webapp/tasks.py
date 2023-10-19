import pendulum
import requests
from django.conf import settings
from django.db.models import Q
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, task

from application.models import Training
from users.models import User


@task()
def test():
    ic("testerei")  # noqa


@task()
def update_close(lead_id: str, data: dict):
    """updates the given close lead with the given data"""
    if settings.STAGE:
        ic("keine Tasks für dev/stage")  # noqa
        return

    ic(lead_id, data)  # noqa
    auth_token = "YXBpXzNQM1ZIbnVua0preHVSdGV5UmMxN2suM2xySHg1SmJIaHhhSTNVekpWM09JNDo6"
    headers = {
        "Authorization": f"Basic {auth_token}",
        "Content-Type": "application/json",
    }
    url = f"https://api.close.com/api/v1/lead/{lead_id}/"
    response = requests.put(url, headers=headers, json=data)
    ic(response.content)  # noqa


def init_close_user(user: User):
    url = f"https://anna.liebendgern.de/admin/users/user/{user.id}/change/"
    ac_email_status_field = "custom.cf_79mOR5o3dSep8ug5RbeFRriZZlCkLURC3yutNXy2L8a"

    data = {
        "url": url,
        ac_email_status_field: "Ja",
    }

    update_close(user.lead_id, data)


@db_periodic_task(crontab(minute="12", hour="3"))
def check_trainings():
    trainings = Training.data.filter(assign_after_days__gt=0)
    for training in trainings:
        check_date = pendulum.now().subtract(days=training.assign_after_days)
        users = User.data.filter(start_date__lt=check_date).filter(~Q(access__training=training))

        if not users:
            ic("heute gibt's niemanden anzupassen")  # noqa

        for user in users:
            access = user.access_set.create(training=training)
            ic(access.user, access)  # noqa
