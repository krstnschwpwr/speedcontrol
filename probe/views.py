from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .forms import SettingsForm
from .models import Speed, AverageQuality, Settings
from .serializers import SpeedSerializer, PrtgSpeedSerializer, SearchSerializer, DictSerializer, QualitySerializer, \
    SettingsSerializer, ErrorMsg, PrtgErrorMsg
from .renderers import PrtgRenderer

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from probe.lib.helpers import is_first_run, is_not_first_run


class QualityList(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = AverageQuality.objects.all().order_by('-id')
    serializer_class = QualitySerializer


class QualityDetail(generics.RetrieveAPIView):
    renderer_classes = [JSONRenderer]

    def retrieve(self, request, *args, **kwargs):
        if not is_first_run():
            queryset = AverageQuality.objects.latest()
            if queryset is None:
               # print('q: {0}'.format(queryset))
                serializer = ErrorMsg('', many=False)
            else:
                serializer = QualitySerializer(queryset, many=False)
        else:
            serializer = ErrorMsg('', many=False)
        return Response(serializer.data)



class SearchView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]

    def list(self, request, *args, **kwargs):
        q = request.GET.get('query', None)
        if q:
            queryset = Speed.objects.all().filter(id__contains=q) | Speed.objects.all().filter(server__contains=q)
        else:
            queryset = Speed.objects.all()
        serializer = SearchSerializer(queryset, many=True)
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
                    serializer = PrtgErrorMsg('', many=False)
                else:
                    serializer = ErrorMsg('', many=False)
        return Response(serializer.data)


class OverviewView(TemplateView):
    def get(self, request):
        if is_first_run():
            return redirect('/start')

        return TemplateResponse(request, 'overview.html')


class RecordView(generics.RetrieveAPIView):
    renderer_classes = [JSONRenderer]

    def retrieve(self, request, *args, **kwargs):
        self.queryset = Settings.objects.last()
        if self.queryset is None:
            serializer = ErrorMsg(self.queryset, many=False)
        else:
            serializer = SettingsSerializer(self.queryset, many=False)
        return Response(serializer.data)


class StartView(TemplateView):
    template_name = 'start.html'


class StatusView(TemplateView):
    model = Speed

    def dispatch(self, request, *args, **kwargs):
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
            expected_upload = request.POST.get('expected_upload', '')
            expected_download = request.POST.get('expected_download', '')
            prtg_url = request.POST.get('prtg_url', '')
            prtg_token = request.POST.get('prtg_token', '')
            if Settings.objects.first():
                ps = Settings.objects.first()
                ps.expected_upload = expected_upload
                ps.expected_download = expected_download
                ps.prtg_url = prtg_url
                ps.prtg_token = prtg_token
                ps.save()
            else:
                prov_object = Settings(expected_upload=expected_upload, expected_download=expected_download, prtg_url=prtg_url,
                                       prtg_token=prtg_token)
                prov_object.save()
        return HttpResponseRedirect('/')
    else:
        form = SettingsForm()
    return render(request, 'settings.html', {
        'form': form,
    })
