import requests
from django.core.management.base import BaseCommand
from django.db.models import Q

from users.models import User


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):

        url = "https://api.close.com/api/v1/data/search/"

        payload = {
            "limit": None,
            "query": {
                "negate": False,
                "queries": [
                    {
                        "negate": False,
                        "object_type": "lead",
                        "type": "object_type"
                    },
                    {
                        "negate": False,
                        "queries": [
                            {
                                "negate": False,
                                "queries": [
                                    {
                                        "condition": {
                                            "object_ids": ["stat_tTavpuXAKbYABanvJFHnbpQmTY4LloW2nmSl74RU8hr"],
                                            "reference_type": "status.lead",
                                            "type": "reference"
                                        },
                                        "field": {
                                            "field_name": "status_id",
                                            "object_type": "lead",
                                            "type": "regular_field"
                                        },
                                        "negate": False,
                                        "type": "field_condition"
                                    }
                                ],
                                "type": "and"
                            }
                        ],
                        "type": "and"
                    }
                ],
                "type": "and"
            },
            "results_limit": 50,
            "sort": [
                {
                    "direction": "desc",
                    "field": {
                        "field_name": "date_created",
                        "object_type": "lead",
                        "type": "regular_field"
                    }
                }
            ],
            "include_counts": True,
            "_limit": 200
        }
        headers = {
            "Authorization": "Basic YXBpXzNQM1ZIbnVua0preHVSdGV5UmMxN2suM2xySHg1SmJIaHhhSTNVekpWM09JNDo6",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        data = response.json()['data']
        # ic(data)

        for lead in data:
            url = f"https://api.close.com/api/v1/lead/{lead['id']}/"

            response = requests.request("GET", url, headers=headers)

            lead_data = response.json()
            for contact in lead_data['contacts']:
                email_filter = Q()

                if not len(contact['emails']):
                    continue

                for email in contact['emails']:
                    email_filter |= Q(email__iexact=email['email'])

                qs = User.data.filter(email_filter)
                ic(qs)

