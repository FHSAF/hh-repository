from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('parse-soup', views.aparser, name='aparser'),
    path('parse-soup/<int:pk>', views.details, name='site-details'),
    path('report/<int:pk>', views.ReportAsPdf, name='page-report'),
]
