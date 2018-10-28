import json
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from background_task import background

from . exchange import ExchangeInterface
from . indicators import Stochastic
from . notifiers import GmailNotifier
from . models import Client
from . models import Signal
from . models import PAIRS
from . models import PERIODS

EI = ExchangeInterface()

@permission_required('is_superuser')
def start_signal(request):
    return render(request, 'signals/start_signal.html',
            {'pairs': PAIRS, 'periods': PERIODS,})

@permission_required('is_superuser')
def start_signal_ajax(request):
    if request.POST.get('start_signal'):
        pair = request.POST.get('pair')
        period = request.POST.get('period')
        check_signals_and_notify_clients(pair, period)
        return HttpResponse(json.dumps({'response': 'Signal is started', 'is_ok': True}))
    else:
        return HttpResponse(json.dumps({'response': 'Wrong request', 'is_ok': False}))

def check_signals_and_notify_clients(pair, period):
    period_in_secs = period_into_secs(period)
    check_signal(pair, period, repeat=period_in_secs, repeat_until=None)

def period_into_secs(period):
    pattern = re.compile('(\d+)([a-zA-Z])')
    matches = pattern.match(period)
    period_number = matches.group(1)
    period_letter = matches.group(2)

    time_values = {
        'm': 60,
        'h': 3600,
        'd': 3600 * 24,
    }

    return time_values[period_letter] * int(period_number)

@background
def check_signal(pair, period):
    historical_data = EI.get_historical_data(pair, period)
    stochastic = Stochastic(historical_data)

    action = stochastic.check_signal()

    if action:
        print(period)
        signal = Signal.objects.create(pair=pair, period=period, action=action)
        notify_clients(signal)

    print("[INFO] {pair} {period}: {action}".format(pair=pair, period=period, action=action))

def notify_clients(signal):
    clients = Client.objects.all()

    clients_emails = [client.email for client in clients if client.email]
    gmail_notifier = GmailNotifier('harry.fexchange@gmail.com', 'changeM20l', clients_emails)
    gmail_notifier.notify(signal.pair, signal.action)