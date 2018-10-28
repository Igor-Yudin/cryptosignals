from django.urls import path

from . views import show_main_page
from . views import subscribe_ajax

urlpatterns = [
    path("", show_main_page, name="show_main_page"),
    path("subscribe_ajax", subscribe_ajax, name="subscribe_ajax"),
]