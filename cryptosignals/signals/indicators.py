class Indicator():
	def __init__(self):
		pass

class Stochastic(Indicator):
	def __init__(self, ohlcv, period=14, overbought=80, oversold=20):
		self.opens = [d[1] for d in ohlcv]
		self.highs = [d[2] for d in ohlcv]
		self.lows = [d[3] for d in ohlcv]
		self.closes = [d[4] for d in ohlcv]
		self.volumes = [d[5] for d in ohlcv]

		self.period = period
		self.overbought = overbought
		self.oversold = oversold

		self.fast_stochastic = self._calc_fast()
		# self.slow_stochastic = self._calc_slow()

	def check_signal(self):
		if (self.fast_stochastic[-2] < self.oversold and
			self.fast_stochastic[-1] > self.oversold):
			return 'BUY'
		elif (self.fast_stochastic[-2] > self.overbought and
			  self.fast_stochastic[-1] < self.overbought):
			return 'SELL'
		else:
			return None

	def _calc_fast(self):
		stochastic_values = []
		for i in range(len(self.opens) - self.period, len(self.opens)):
			start_index = i - self.period + 1
			last_index = start_index + self.period

			lowest = min(self.lows[start_index:last_index])
			highest = max(self.highs[start_index:last_index])

			current = self.closes[i]

			try:
				value = (current - lowest) / (highest - lowest) * 100
			except ZeroDivisionError:
				value = 0.5
			stochastic_values.append(value)
		return stochastic_values

	# def _calc_slow(self):
		# return None

	def get_line(self):
		return self.fast_stochastic