from django.db import models


PAIRS = (
	("BTC/USD", "BTC/USD"),
)

ACTIONS = (
	("BUY", "BUY"),
	("SELL", "SELL"),
)

PERIODS = (
	("5 minute", "5m"),
	("10 minutes", "10m"),
	("15 minutes", "15m"),
	("30 minutes", "30m"),
	("1 hour", "1h"),
	("4 hours", "4h"),
	("1 day", "1d"),
)

class Signal(models.Model):
	pair = models.CharField(choices=PAIRS, max_length=10, default="BTC/USD")
	time = models.DateTimeField(auto_now_add=True)
	action = models.CharField(choices=ACTIONS, max_length=5, default="BUY")
	period = models.CharField(choices=PERIODS, max_length=5, default="5m")

class Client(models.Model):
	email = models.CharField(max_length=50, default="", blank=True)
	# telegram = models.CharField(max_length=50, default="", blank=True)
	# slack = models.CharField(max_length=50, default="", blank=True)