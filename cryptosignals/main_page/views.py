import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from signals.models import Client

def show_main_page(request):
    return render(request, 'main_page/main_page.html')

def subscribe_ajax(request):
    if request.POST.get('subscribe'):
        email = request.POST.get('email')
        telegram = request.POST.get('telegram')
        slack = request.POST.get('slack')

        client = Client.objects.create(email=email, telegram=telegram, slack=slack)

        return HttpResponse(json.dumps({"is_ok": True}))
    else:
        return HttpResponse(json.dumps({"is_ok": False}))

def login(request):
    return redirect('/admin/login')