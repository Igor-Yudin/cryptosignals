import re
import time
from datetime import datetime, timedelta, timezone


import ccxt
from tenacity import retry, retry_if_exception_type, stop_after_attempt


class ExchangeInterface():
    """Interafce for perfoming queries against exchange API.
    """
    def __init__(self):
        self.exchange = ccxt.bittrex({'verobse': True})
        self.timeframes = ['5m', '30m', '1h', '1d']

    @retry(retry=retry_if_exception_type(ccxt.NetworkError), stop=stop_after_attempt(3))
    def get_historical_data(self, market_pair, time_unit, start_date=None, max_periods=100):
        """Get historical OHLCV for a market pair.
        """
        if time_unit not in self.timeframes:
            raise ValueError(
                "There is no support for {time_unit} timeframe.".format(
                    time_unit=time_unit
                )
            )

        if not start_date:
            timeframe_regex = re.compile('([0-9]+)([a-zA-Z])')
            timeframe_matches = timeframe_regex.match(time_unit)
            time_quantity = timeframe_matches.group(1)
            time_period = timeframe_matches.group(2)

            timedelta_values = {
                'm': 'minutes',
                'h': 'hours',
                'd': 'days',
                'w': 'weeks',
                'M': 'months',
                'y': 'years'
            }

            timedelta_args = { timedelta_values[time_period]: int(time_quantity) }

            start_date_delta = timedelta(**timedelta_args)

            max_days_date = datetime.now() - (max_periods * start_date_delta)
            start_date = int(max_days_date.replace(tzinfo=timezone.utc).timestamp() * 1000)

        historical_data = self.exchange.fetch_ohlcv(
                                            market_pair,
                                            timeframe=time_unit,
                                            since=start_date
                                        )

        if not historical_data:
            raise ValueError("No historical data provided.")

        historical_data.sort(key=lambda d: d[0])

        time.sleep(self.exchange.rateLimit / 1000)

        return historical_data