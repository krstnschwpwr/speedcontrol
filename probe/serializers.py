from django.utils import formats
from rest_framework import serializers
from .models import Speed, AverageQuality
from .lib.pyspeedtest import pretty_speed
from .models import Settings


class DictSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return instance


class PrtgSpeedSerializer(serializers.ModelSerializer):
    prtg = serializers.SerializerMethodField('struc')

    def struc(self, obj):
        filters = ['server', 'time', 'id']
        channels = []
        relevant_fields = [field.name for field in Speed._meta.fields if field.name not in filters]
        for field in relevant_fields:
            if field == 'ping':
                channels.append({"channel": str(field),
                                 "value": getattr(obj, str(field)),
                                 "float": 1,
                                 "customUnit": "Mbit/s" if field != 'ping' else "ms"})
            else:
                channels.append({"channel": str(field),
                                 "value": pretty_speed(getattr(obj, str(field)) * 0.000001),
                                 "float": 1,
                                 "customUnit": "Mbit/s" if field != 'ping' else "ms"})
        prtg = {"result": channels}
        return prtg

    class Meta:
        model = Speed
        fields = ['prtg']


class SpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speed
        fields = ('id', 'server', 'time', 'ping', 'upload', 'download')


class SearchSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_title(self, obj):
        return '#{0} - {1}'.format(obj.id, obj.server)

    def get_description(self, obj):
        return formats.date_format(obj.time, "SHORT_DATETIME_FORMAT")

    def get_url(self, obj):
        return '/api/v1/measurements/{0}'.format(obj.id)

    class Meta:
        model = Speed
        fields = ('id', 'server', 'time', 'ping', 'upload', 'download', 'title', 'description', 'url')


class QualitySerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField('perc')

    def perc(self, obj):
        provided = Settings.objects.first()
        sum_expected_speed = provided.expected_download + provided.expected_upload
        sum_avg_speed = (obj.avg_download + obj.avg_upload)
        q = sum_avg_speed * 100 / sum_expected_speed
        return q

    class Meta:
        model = AverageQuality
        fields = ('id', 'time', 'avg_download', 'avg_upload', 'percentage')
