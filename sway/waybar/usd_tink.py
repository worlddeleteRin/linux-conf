#!/usr/bin/env python3

import logging
import sys
import json
from httpx import Client, Request, Response
import argparse
import time
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# necessary variable
access_token = ''
main_acc_id = '2159091681'
base_url = 'https://invest-public-api.tinkoff.ru/rest'
sub_url = 'tinkoff.public.invest.api.contract.v1.'
usd_figi = 'BBG0013HGFT4'
eur_figi = 'BBG0013HJJ31'
# f'Authorization: Bearer {access_token}'

# content variables
class CurrencyRates(BaseModel):
    usd_rate: str = "no data yet..."
    eur_rate: str = "no data yet..."

    def main_output(self) -> dict:
        text = f'{self.usd_rate}'
        cls = ""
        output = {
            'text': text,
            'class': cls
        }
        return output

currency_rates = CurrencyRates()

def init_http_client() -> Client:
    client = Client(
        base_url=base_url,
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
    )
    return client

def request_currency_rates(http: Client):
    global currency_rates 
    url = f'{sub_url}MarketDataService/GetLastPrices'
    data = {
        'figi': [
            usd_figi,
            eur_figi
        ]
    }
    resp: Response = http.post(
        url=url,
        json=data
    )
    try:
        r = resp.json()['lastPrices']
        if not isinstance(r, list):
            logger.warning(f'resp is {r}')
            raise Exception("response is not dict")

        usd_rate = float(f'{r[0]["price"]["units"]}.{r[0]["price"]["nano"]}')
        eur_rate = float(f'{r[1]["price"]["units"]}.{r[1]["price"]["nano"]}')

        currency_rates.usd_rate = str(usd_rate)
        currency_rates.eur_rate = str(eur_rate)
        # total_portfolio_yield = 12

    except Exception as e:
        logger.warning(f'error {e}, resp is {resp.content}')

def output_main_info():
    global currency_rates 

    sys.stdout.write(json.dumps(currency_rates.main_output())+ '\n')
    sys.stdout.flush()

def get_info(client: Client):
    request_currency_rates(client)
    output_main_info()

def main():
    # arguments = parse_arguments()
    logging.basicConfig(
        level=logging.DEBUG
        # level=logging.WARNING
    )
    logger.debug('Starting tink script')
    http_client = init_http_client()
    # logger.debug('Http client initialized')
    while True:
        get_info(http_client)
        time.sleep(5)

if __name__ == '__main__': 
    main()
