from django.core.management.base import BaseCommand
from django.utils import timezone
from probe.lib import pyspeedtest
from probe.models import Speed, AverageQuality
from datetime import datetime, timedelta
from probe.lib.helpers import is_first_run


def fill():
    if is_first_run():
        return
    speed_values = pyspeedtest.SpeedTest()
    ping = round(speed_values.ping())
    download = round(speed_values.download())
    upload = round(speed_values.upload())
    entry = Speed(time=timezone.now(), server=speed_values.host, ping=ping, download=download, upload=upload)
    entry.save()


def calc_qos():
    if is_first_run():
        return
    last_24 = Speed.objects.all().filter(time__gte=datetime.now() - timedelta(days=1))
    avg_down = 0
    avg_up = 0
    for o in last_24:
        avg_down += o.download
        avg_up += o.upload
    avg_down /= len(last_24)
    avg_up /= len(last_24)
    qos = AverageQuality(time=timezone.now(), avg_download=avg_down, avg_upload=avg_up)
    qos.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        fill()
        calc_qos()



