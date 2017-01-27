from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .forms import SettingsForm
from .models import Speed, AverageQuality, Settings
from .serializers import SpeedSerializer, PrtgSpeedSerializer, SearchSerializer, DictSerializer, QualitySerializer
from .renderers import PrtgRenderer

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from probe.lib.helpers import is_first_run


class QualityList(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = AverageQuality.objects.all().order_by('-id')
    serializer_class = QualitySerializer


class QualityDetail(generics.RetrieveAPIView):
    renderer_classes = [JSONRenderer]

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if id:
            queryset = AverageQuality.objects.get(id=id)
            serializer = QualitySerializer(queryset, many=False)
        else:
            queryset = AverageQuality.objects.latest()
            serializer = QualitySerializer(queryset, many=False)

        return Response(serializer.data)


class SearchView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]

    def list(self, request, *args, **kwargs):
        q = request.GET.get('query', None)
        if q:
            queryset = Speed.objects.all().filter(id__contains=q) | Speed.objects.all().filter(server__contains=q)
        else:
            queryset = Speed.objects.all()
        serializer = SearchSerializer(queryset , many=True)
        return Response({'results': serializer.data})


class SpeedList(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = Speed.objects.all()
    serializer_class = SpeedSerializer


class SpeedDetail(generics.RetrieveAPIView):
    renderer_classes = [JSONRenderer, PrtgRenderer]

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        format = request.GET.get('format', None)
        if id:
            queryset = Speed.objects.get(id=id)
            serializer = SpeedSerializer(queryset, many=False)
        else:
            try:
                queryset = Speed.objects.latest()
                if format == 'prtg':
                    serializer = PrtgSpeedSerializer(queryset, many=False)
                else:
                    serializer = SpeedSerializer(queryset, many=False)
            except:
                if format == 'prtg':
                    serializer = DictSerializer({'prtg': {'error': 1, 'text': 'No data available!'}}, many=False)
                else:
                    serializer = DictSerializer({'message': 'No data available!', 'status': 500}, many=False)

        return Response(serializer.data)


class OverviewView(TemplateView):
    def get(self, request):
        if is_first_run():
            return redirect('/start')

        return TemplateResponse(request, 'overview.html')


class StartView(TemplateView):
    template_name = 'start.html'


class StatusView(TemplateView):
    model = Speed

    def get(self, request):
        if is_first_run():
            return redirect('/start')

        return TemplateResponse(request, 'status.html', context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)
        context['exp'] = Settings.objects.latest()
        return context


def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            upload = request.POST.get('upload', '')
            download = request.POST.get('download', '')
            prtg_url = request.POST.get('prtg_url', '')
            prtg_token = request.POST.get('prtg_token', '')
            if Settings.objects.first():
                ps = Settings.objects.first()
                ps.upload = upload
                ps.download = download
                ps.prtg_url = prtg_url
                ps.prtg_token = prtg_token
                ps.save()
            else:
                prov_object = Settings(expected_upload=upload, expected_download=download, prtg_url=prtg_url, prtg_token=prtg_token)
                prov_object.save()
        return HttpResponseRedirect('/')
    else:
        form = SettingsForm()
    return render(request, 'settings.html', {
        'form': form,
    })