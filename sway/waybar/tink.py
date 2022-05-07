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
# f'Authorization: Bearer {access_token}'

# content variables
class Portfolio(BaseModel):
    total_amount: str = "no data yet..."
    total_yield_amount: str = "..."
    total_yield_percent: str = "..."

    def set_total_amount(self, amount: float):
        self.total_amount = str(round(amount,2))
    def calc_yield_amount(self):
        percent = float(self.total_yield_percent)
        self.total_yield_amount = str(round((float(self.total_amount) * percent * 0.01), 2))
        pass

    def set_yield_percent(self, percent: float):
        self.total_yield_percent = str(percent)
        self.calc_yield_amount()

    def main_output(self) -> dict:
        text = f'{self.total_amount} {self.total_yield_amount} ({self.total_yield_percent})'
        p = float(self.total_yield_percent)
        cls = ""
        if p < 0:
            cls = "total-down"
        else:
            cls = "total-up"
        output = {
            'text': text,
            'class': cls
        }
        return output

portfolio = Portfolio()

def init_http_client() -> Client:
    client = Client(
        base_url=base_url,
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
    )
    return client

def request_portfolio(http: Client):
    global portfolio 
    url = f'{sub_url}OperationsService/GetPortfolio'
    data = {
        'accountId': main_acc_id
    }
    resp: Response = http.post(
        url=url,
        json=data
    )
    try:
        r = resp.json()
        if not isinstance(r, dict):
            logger.warning(f'resp is {r}')
            raise Exception("response is not dict")

        total_shares = float(f'{r["totalAmountShares"]["units"]}.{r["totalAmountShares"]["nano"]}')
        total_currencies = float(f'{r["totalAmountCurrencies"]["units"]}.{r["totalAmountCurrencies"]["nano"]}')
        total_amount = total_shares + total_currencies
        total_yield_percent = float(f'{r["expectedYield"]["units"]}.{abs(int(r["expectedYield"]["nano"]))}')

        portfolio.set_total_amount(total_amount)
        portfolio.set_yield_percent(total_yield_percent)
        # total_portfolio_yield = 12

    except Exception as e:
        logger.warning(f'error {e}, resp is {resp.content}')

def output_main_info():
    global portfolio

    sys.stdout.write(json.dumps(portfolio.main_output())+ '\n')
    sys.stdout.flush()

"""
def parse_arguments():
    parser = argparse.ArgumentParser()

    # Increase verbosity with every occurrence of -v
    parser.add_argument('-v', '--verbose', action='count', default=0)

    # Define for which player we're listening
    parser.add_argument('--player')

    return parser.parse_args()
"""
def get_info(client: Client):
    request_portfolio(client)
    output_main_info()

def main():
    # arguments = parse_arguments()
    logging.basicConfig(
        level=logging.DEBUG
        # level=logging.WARNING
    )
    # Initialize logging
    """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                        format='%(name)s %(levelname)s %(message)s')
    """

    # Logging is set by default to WARN and higher.
    # With every occurrence of -v it's lowered by one
    # logger.setLevel(max((3 - arguments.verbose) * 10, 0))

    # logger.debug('Starting tink script')
    http_client = init_http_client()
    # logger.debug('Http client initialized')
    while True:
        get_info(http_client)
        time.sleep(5)
    # logger.debug(f'Total portfolio is {total_portfolio}')

if __name__ == '__main__': 
    main()
