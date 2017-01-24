from django.db import models
from django.utils import timezone


class Settings(models.Model):
    expected_upload = models.IntegerField(db_column='upload', blank=False)
    expected_download = models.IntegerField(db_column='download', blank=False)
    prtg_url = models.URLField(db_column='prtg_url', blank=True)
    prtg_token = models.CharField(db_column='prtg_token', blank=True, max_length=255)

    class Meta:
        get_latest_by = 'id'

    def __unicode__(self):
        return str(self.prtg_token)


class Speed(models.Model):
    time = models.DateTimeField(default=timezone.now)
    server = models.CharField(db_column='server', help_text='Server Location', max_length=255)
    ping = models.IntegerField(db_column='ping', help_text='Ping in ms', blank=False)
    download = models.IntegerField(db_column='download', help_text='Download Speed in Bit/s', blank=False)
    upload = models.IntegerField(db_column='upload', help_text='Upload Speed in Bit/s', blank=False)

    class Meta:
        get_latest_by = 'id'

    def __unicode__(self):
        return self.server


class AverageQuality(models.Model):
    time = models.DateTimeField(default=timezone.now)
    avg_download = models.IntegerField(db_column='avg_download', help_text='Download Speed in Bit/s', blank=False)
    avg_upload = models.IntegerField(db_column='avg_upload', help_text='Upload Speed in Bit/s', blank=False)

    class Meta:
        get_latest_by = 'id'

    def __unicode__(self):
        return self.avg_upload

    def get_qos_percentage(self):
        l = Settings.objects.latest()
        filters = ['id']
        data = []
        relevant_f = [field.name for field in Settings._meta.fields if field.name not in filters]
        for field in relevant_f:
            data.append(getattr(l, str(field)))
        exp_up = data[0]
        exp_down = data[1]

        sum_expected_speed = exp_up + exp_down
        sum_avg_speed = (self.avg_download + self.avg_upload)
        q = round(sum_avg_speed * 100 / sum_expected_speed)
        print(q)
        return q
