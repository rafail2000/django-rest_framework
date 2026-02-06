import json

import currencyapicom
import warnings
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def convert_currencies(rub_price):

    client = currencyapicom.Client('cur_live_Mz7TK4kUlsgj175aITPksfJVPrqQ2ObV9ZEv0kUC')
    result = client.latest(['RUB'])
    usd_rate = result["data"]["RUB"]["value"]
    print(usd_rate)
    usd_price = rub_price/usd_rate

    return usd_price

def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every = 10,
        period = IntervalSchedule.SECONDS,
    )
    PeriodicTask.objects.create(
    interval = schedule,  # we created this above.
    name = 'Importing contacts',  # simply describes this periodic task.
    task = 'proj.tasks.import_contacts',  # name of task.
    args = json.dumps(['arg1', 'arg2']),
    kwargs = json.dumps({
    'be_careful': True,}),
    expires = datetime.utcnow() + timedelta(seconds=30))
