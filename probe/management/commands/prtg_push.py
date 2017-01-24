import json
import logging
import requests
from django.core.management.base import BaseCommand
from probe.models import Speed, Settings
from probe.serializers import PrtgSpeedSerializer
from probe.lib.helpers import is_first_run, use_prtg


def push():
    if is_first_run() or not use_prtg():
        return

    logging.basicConfig(level=logging.DEBUG)
    queryset = Speed.objects.latest()
    prtg_settings = Settings.objects.first()

    payload = json.dumps(PrtgSpeedSerializer(queryset, many=False).data)
    resp = requests.get("{0}{1}?content={2}".format(prtg_settings.prtg_url, prtg_settings.prtg_token, payload))

    if resp.status_code == 200 and 'application/json' in resp.headers['content-type']:
        a = resp.json()
        if 'status' in a.keys() and a["status"] == "Ok":
            return 0
    return 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        push()