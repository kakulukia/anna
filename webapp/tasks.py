import requests
from huey.contrib.djhuey import task


@task()
def update_close(lead_id: str, data: dict):
    ic(data)
    headers = {
        "Authorization": "Basic YXBpXzNQM1ZIbnVua0preHVSdGV5UmMxN2suM2xySHg1SmJIaHhhSTNVekpWM09JNDo6",
        "Content-Type": "application/json"
    }
    url = f"https://api.close.com/api/v1/lead/{lead_id}/"
    response = requests.put(url, headers=headers, json=data)
    ic(response.content)


def test_task():
    lead_id = "lead_t0UL605Vh3qZWgSQOPOw5nCI0XxRTwiBn61OyIhRyDC"
    data = {
        "url": "https://anna.liebendgern.de/",
        "custom.cf_Ps3oP5tcq7QwWgOPzsFdaDBK9zDC4Gpga4ozsh0xXQb": 17
    }
    update_close(lead_id, data)
