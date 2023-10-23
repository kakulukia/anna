from users.models import User
from webapp.tasks import update_close


def update_last_login(sender, instance: User, **kwargs):
    if not instance.lead_id or not instance.last_login:
        return

    old_user = User.data.get(id=instance.id)

    if not old_user.last_login or instance.last_login.date() != old_user.last_login.date():
        data = {"custom.cf_PnRnq2gTqYTGElh7iX0MIQshSQtXUmqPDLjYy5Dtqt2": instance.last_login.date().isoformat()}
        update_close(instance.lead_id, data)
