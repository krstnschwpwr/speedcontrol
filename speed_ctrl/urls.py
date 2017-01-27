from django.conf.urls import url
from probe import views

urlpatterns = [
    url(r'^api/v1/qualityofservice/latest', views.QualityDetail.as_view()),
    url(r'^api/v1/qualityofservice/(?P<id>[0-9]+)', views.QualityDetail.as_view()),
    url(r'^api/v1/qualityofservice[/]?$', views.QualityList.as_view()),

    url(r'^api/v1/measurements/latest', views.SpeedDetail.as_view()),
    url(r'^api/v1/measurements/(?P<id>[0-9]+)', views.SpeedDetail.as_view()),
    url(r'^api/v1/measurements[/]?$', views.SpeedList.as_view()),

    url(r'^search(?P<query>[a-zA-Z0-9\.]+)?$', views.SearchView.as_view()),
    url(r'^settings', views.settings, name="settings"),
    url(r'^overview', views.OverviewView.as_view()),
    url(r'^start', views.StartView.as_view()),
    url(r'^$', views.StatusView.as_view())
]