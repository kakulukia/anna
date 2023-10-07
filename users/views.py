import json
from typing import List

import dateutil.parser
import pendulum
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from prodict import Prodict

from application.models import Product
from my_secrets import secrets
from users.models import User
from webapp.tasks import init_close_user


class Email(Prodict):
    email: str
    type: str


class Contact(Prodict):
    id: str
    lead_id: str
    display_name: str
    emails: List[Email]


@csrf_exempt
def create_or_update_lead_webhook(request):
    def get_contact_data(contact_ids):
        auth_token = "YXBpXzNQM1ZIbnVua0preHVSdGV5UmMxN2suM2xySHg1SmJIaHhhSTNVekpWM09JNDo6"
        headers = {
            "Authorization": f"Basic {auth_token}",
            "Content-Type": "application/json",
        }
        url = "https://api.close.com/api/v1/contact/"
        data = []
        for id in contact_ids:
            response = requests.get(url + id, headers=headers)
            data.append(Contact.from_dict(response.json()))
        return data

    def parse_duration(string: str):
        parts = string.split("-")
        end = dateutil.parser.parse(parts[1], dayfirst=True)
        start_string = parts[0] + (str(end.year) if not parts[0].split(".")[-1] else "")
        start = dateutil.parser.parse(start_string, dayfirst=True)
        if start > end:
            start = pendulum.instance(start, tz="local").subtract(years=1)
        return start, end

    def get_users(lead_id: str, contact_ids: list) -> List[User]:
        users = []

        qs = User.data.filter(lead_id=event.lead_id)
        if qs.count() == 2:
            return qs
        else:
            # contacts not present > create user objects
            contacts = get_contact_data(contact_ids)

            for contact in contacts:
                if not contact.emails:
                    continue

                qs = User.data.filter(contact_id=contact.id)

                # try to find user via contact id
                if qs:
                    user = qs.get()
                else:
                    # try to find an existing contact via email
                    names = contact.display_name.split(" ")
                    email = contact.emails[0].email

                    qs = User.data.filter(email__iexact=email)
                    if qs:
                        user = qs.get()
                    else:
                        # otherwise crate a new user
                        user = User.data.create(
                            email=email,
                            first_name=" ".join(names[:-1]),
                            last_name=names[-1],
                            username=email,
                        )
                        # new users get a default password
                        user.set_password(secrets.DEFAULT_USER_PASSWORD)

                user.contact_id = contact.id
                user.lead_id = contact.lead_id
                user.save()

                init_close_user(user)

                users.append(user)

        return users

    if request.content_type == "application/json":
        data = json.loads(request.body)

        event = Prodict.from_dict(data).event
        ic(event)  # noqa
        duration_field = "custom.cf_8zV6c7eijjmYfIbl1w1vfLzZunknUoLs4sb13uoOubp"
        purchase_options = (
            "custom.cf_0eKueP25HDy5wnHDeZXB7ySzrlx3JhiQXjaczfIx2a1"  # Feld Kaufaktionen
        )
        zoom_link = "custom.cf_fsbXp5btDzxOJqP9QKmCNa62vc4MnHevvpXnkMkWMB8"

        # only listen for Kaufaktionen being added or removed
        if (purchase_options in event.data) or (
            purchase_options not in event.data
            and "previous_data" in event
            and purchase_options in event.previous_data
        ):
            options = event.data[purchase_options] if purchase_options in event.data else []
            users = get_users(event.lead_id, event.data.contact_ids)

            for user in users:
                if zoom_link in event.data:
                    user.zoom_link = event.data[zoom_link]
                    user.save()

                # now lets set or update the duration
                if duration_field in event.data:
                    start, end = parse_duration(event.data[duration_field])

                    user.start_date = start
                    user.end_date = end
                    user.save()

                # for all listed products -> add access
                for product in Product.data.all():
                    # add access for all listed products
                    if product.name in options or product.free:
                        ic(f"adding {product.name}")  # noqa
                        if not user.bought_teaser and product.teaser:
                            user.bought_teaser = True
                            user.save()
                        if not user.bought_membership and product.membership:
                            user.bought_membership = True
                            user.save()

                        for course in product.courses.all():
                            access, new = user.access_set.get_or_create(training=course)
                            ic(f"adding {access, new}")  # noqa

                    # remove access for all products not listed
                    elif product.name not in options and not product.free:
                        ic(f"removing {product.name}")  # noqa
                        for course in product.courses.all():
                            user.access_set.filter(training=course).delete()

        return HttpResponse(status=202)
    else:
        return HttpResponse(status=400, content="Content-Type must be application/json")
