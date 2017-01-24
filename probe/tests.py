from probe.models import Speed, AverageQuality, Settings
from django.test import TestCase
from rest_framework.test import APITestCase
import json
from django.utils import timezone
from .views import is_first_run
import requests

MODELS = [Speed, AverageQuality, Settings]


class DatabaseConnectionTestCase(TestCase):
    def test_speed_model_con(self):
        w = Speed.objects.create(time=timezone.now(), server="Servername", ping="23123", download="3423423",
                                 upload="3423423")
        k = Speed.objects.latest()
        self.assertEqual(k, w)

    def test_quality_model_con(self):
        w = AverageQuality.objects.create(time=timezone.now(), avg_download="3423423", avg_upload="3423423")
        k = AverageQuality.objects.latest()
        self.assertEqual(k, w)

    def test_settings_model_con(self):
        w = Settings.objects.create(expected_upload="3423423", expected_download="3423423",
                                    prtg_url="http://www.google.de", prtg_token="3sdf4sdfw")
        k = Settings.objects.latest()
        self.assertEqual(k, w)


class WebViewTestCase(TestCase):
    def test_status_view_when_first_run(self):
        k = is_first_run()
        response = self.client.get("/")
        self.assertEqual(k, True)
        self.assertRedirects(response, "/settings", status_code=302, target_status_code=200)

    def test_status_view_when_not_first_run(self):
        Settings.objects.create(expected_download="34234", expected_upload="34234")
        k = is_first_run()
        response = self.client.get("/")
        self.assertEqual(k, False)
        self.assertTemplateUsed(response, 'status.html')
        self.assertEqual(response.status_code, 200)

    def test_overview_view_when_first_run(self):
        k = is_first_run()
        response = self.client.get("/overview")
        self.assertEqual(k, True)
        self.assertRedirects(response, "/settings", status_code=302, target_status_code=200)

    def test_overview_view_when_not_first_run(self):
        Settings.objects.create(expected_download="34234", expected_upload="34234")
        k = is_first_run()
        response = self.client.get("/overview")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(k, False)
        self.assertTemplateUsed(response, 'overview.html')

    def test_settings_view_general(self):
        response = self.client.get("/settings")
        self.assertEqual(response.status_code, 200)


class ApiTestCase(APITestCase):
    maxDiff = None

    def test_latest_json_measurement(self):
        k = Speed.objects.create(time=timezone.now(), server="Servername", ping="27",
                             upload="2893574", download="14306788")
        response = requests.get('http://127.0.0.1:8000/api/v1/measurements/latest?format=json')
        json_re = response.json()
        lk = len(json_re)
        if lk == 0:
            self.assertEqual(response.status_code, 200)
        type = response.headers['content-type']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_re, k)
        self.assertTrue(type, 'application/json')
        one_entry = Speed.objects.all()
        self.assertTrue(one_entry.count(), 1)

    def test_all_json_measurements(self):
        Speed.objects.create(time=timezone.now(), server="Servername", ping="23123", download="3423423",
                             upload="3423423")
        Speed.objects.create(time=timezone.now(), server="Testi", ping="342", download="342342",
                             upload="67567")
        Speed.objects.create(time=timezone.now(), server="Test34", ping="3", download="3423",
                             upload="898")
        response = requests.get('http://127.0.0.1:8000/api/v1/measurements/')
        self.assertEqual(response.status_code, 200)
        saved_speed_el = Speed.objects.all()
        self.assertEqual(saved_speed_el.count(), 3)
        type = response.headers['content-type']
        self.assertTrue(type, 'application/json')

    def test_latest_prtg_json_entry(self):
        k = Speed.objects.create(time=timezone.now(), server="Servername", ping="27", download="14306788",
                             upload="2893574")
        response = requests.get('http://127.0.0.1:8000/api/v1/measurements/latest?format=prtg')
        prtg_json_re = response.json()
        print(prtg_json_re)
        self.assertTrue(prtg_json_re, k)
        self.assertEqual(response.status_code, 200)

    def test_empty_json(self):
        response = self.client.get('/api/v1/measurements/latest/')
        error_msg = json.loads('{"message":"No data available!","status":500}')
        empty_prtg_re = response.json()
        self.assertEqual(empty_prtg_re, error_msg)
        self.assertEqual(response.status_code, 200)
