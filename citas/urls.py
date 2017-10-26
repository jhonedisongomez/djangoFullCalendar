from django.conf.urls import url
from .views import CitasView
from django.conf import settings


urlpatterns = [

    
    url(r'^asistencia/$', VerifySignUpActivity.as_view(),name='activities'),
]
