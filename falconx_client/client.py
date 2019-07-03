import base64
import hashlib
import hmac
import time

import requests
from requests import Response
from requests.auth import AuthBase


class FalconxClient:
    URL = "https://api.falconx.io/v1/"

    def __init__(self, key, secret, passphrase):
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.auth = FXRfqAuth(self.key, self.secret, self.passphrase)

    def _process_response(self, response: Response):

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('API call failed with status: {} - text: {}'.format(response.status_code, response.text))

    def get_trading_pairs(self):
        response = requests.get(self.URL + 'pairs', auth=self.auth)
        return self._process_response(response)

    def get_quote(self, base, quote, quantity, side):
        """
        Get a quote for a token pair.
        :param base: (str) base token e.g. BTC, ETH
        :param quote: (str) quote token e.g. USD, BTC
        :param quantity: (float, Decimal)
        :param side: (str) two-way, buy, sell
        :return:
        """
        params = {
            'token_pair': {
                'base_token': base,
                'quote_token': quote
            },
            'quantity': {
                'token': base,
                'value': str(quantity)
            },
            'side': side
        }

        response = requests.post(self.URL + 'quotes', json=params, auth=self.auth)
        return self._process_response(response)

    def execute_quote(self, fx_quote_id, side):
        """
        Execute the trade.
        :param fx_quote_id: (str) the quote id received via get_quote
        :param side: (str) must be either buy or sell
        :return:
        """
        params = {
            'fx_quote_id': fx_quote_id,
            'side': side
        }

        response = requests.post(self.URL + 'quotes/execute', json=params, auth=self.auth)
        return self._process_response(response)

    def get_quote_status(self, fx_quote_id):
        """
        :param fx_quote_id: (str) the quote id received via get_quote
        :return:
        """

        return self._process_response(requests.get(self.URL + 'quotes/{}'.format(fx_quote_id), auth=self.auth))

    def get_executed_quotes(self, t_start, t_end):
        """
        :param t_start: (str) time in ISO8601 format
        :param t_end: (str)
        :return:
        """
        params = {'t_start': t_start, 't_end': t_end}
        return self._process_response(requests.get(self.URL + 'quotes', params=params, auth=self.auth))

    def get_balances(self):
        """
        Get account balances.
        :return:
        """
        return self._process_response(requests.get(self.URL + 'balances', auth=self.auth))


# Create custom authentication for RFQ
class FXRfqAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        request_body = request.body.decode() if request.body else ''
        message = timestamp + request.method + request.path_url + request_body
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())

        request.headers.update({
            'FX-ACCESS-SIGN': signature_b64,
            'FX-ACCESS-TIMESTAMP': timestamp,
            'FX-ACCESS-KEY': self.api_key,
            'FX-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


def main():
    pass


if __name__ == '__main__':
    main()
