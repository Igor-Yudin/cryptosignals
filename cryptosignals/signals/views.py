import json
import re
import os
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from background_task import background

from . exchange import ExchangeInterface
from . indicators import Stochastic
from . notifiers import GmailNotifier, SlackNotifier, TelegramNotifier
from . models import Client
from . models import Signal
from . models import PAIRS
from . models import PERIODS
from . models import ACTIONS

EI = ExchangeInterface()
MAILGUN_API = os.environ['MAILGUN_API']

@permission_required('is_superuser')
def start_signal(request):
    return render(request, 'signals/start_signal.html',
            {'pairs': PAIRS, 'periods': PERIODS, 'actions': ACTIONS})

@permission_required('is_superuser')
def start_signal_ajax(request):
    if request.POST.get('start_signal'):
        pair = request.POST.get('pair')
        period = request.POST.get('period')
        _check_signals_and_notify_clients(pair, period)
        return HttpResponse(json.dumps({'response': 'Signal is started', 'is_ok': True}))
    else:
        return HttpResponse(json.dumps({'response': 'Wrong request', 'is_ok': False}))

def _check_signals_and_notify_clients(pair, period):
    period_in_secs = _period_into_secs(period)
    _check_signal(pair, period, repeat=period_in_secs, repeat_until=None)

def _period_into_secs(period):
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
def _check_signal(pair, period):
    historical_data = EI.get_historical_data(pair, period)
    stochastic = Stochastic(historical_data)

    action = stochastic.check_signal()

    if action:
        signal = Signal.objects.create(pair=pair, period=period, action=action)
        _notify_clients(signal)

    print("[INFO] {pair} {period}: {action}".format(pair=pair, period=period, action=action))

def _notify_clients(signal):
    message_subject = signal.pair
    message_text = '{signal_pair}: {signal_action} in next {signal_period}'.format(signal_pair=signal.pair,
                                                                                   signal_action=signal.action,
                                                                                   signal_period=signal.period)
    clients = Client.objects.all()

    clients_emails = [client.email for client in clients if client.email]
    for email in clients_emails:
        _send_email_message(email, message_subject, message_text)

    slack_notifier = SlackNotifier('https://hooks.slack.com/services/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')
    slack_notifier.notify(message_text)

    telegram_nitifier = TelegramNotifier('629041496:AAGrh2aLn5ix1ZQK48iwkg7u53nHXje7qxQ', '-305542134', None)
    telegram_nitifier.notify(message_text)

def _send_email_message(email_to, subject, text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa509ca0a228442788c042d4835c9ea15.mailgun.org/messages",
        auth=("api", MAILGUN_API),
        data={"from": "CryptoSignals <harry.fexchange@gmail.com>",
              "to": "<{email_to}>".format(email_to=email_to),
              "subject": subject,
              "text": text})

@permission_required('is_superuser')
def emit_signal_ajax(request):
    if request.POST.get('emit_signal'):
        pair = request.POST.get('pair')
        period = request.POST.get('period')
        action = request.POST.get('action')

        signal = Signal.objects.create(pair=pair, period=period, action=action)
        _notify_clients(signal)

        signal.delete()

        return HttpResponse(json.dumps({'response': 'Signal is emited', 'is_ok': True}))
    else:
        return HttpResponse(json.dumps({'response': 'Wrong request', 'is_ok': False}))