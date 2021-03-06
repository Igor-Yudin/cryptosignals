from django.contrib import admin
from django.urls import path

from . views import start_signal
from . views import start_signal_ajax
from . views import emit_signal_ajax

urlpatterns = [
    path('start_signal', start_signal, name='start_signal'),
    path('start_signal_ajax', start_signal_ajax, name='start_signal_ajax'),
    path('emit_signal_ajax', emit_signal_ajax, name='emit_signal_ajax'),
]