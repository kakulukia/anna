from users.models import User
from webapp.tasks import update_close


def update_last_login(sender, instance: User, **kwargs):
    data = {"custom.cf_PnRnq2gTqYTGElh7iX0MIQshSQtXUmqPDLjYy5Dtqt2": instance.last_login.date().isoformat()}
    update_close(instance.lead_id, data)
