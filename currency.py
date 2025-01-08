from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

from constraints import USD_FIELDS


def get_currency() -> dict[str, list]:
    """Returns currency -> (Buy, Sell)"""
    url = 'https://vernadka-valyuta.ru/'
    headers = {'User-Agent': UserAgent().random}
    r = requests.get(
        url=url,
        headers=headers
    )
    if r.status_code != 200:
        raise ConnectionError(f"Status code: {r.status_code}")
    soup = BeautifulSoup(r.text, 'lxml')
    currencies = {}
    for name, fields in USD_FIELDS.items():
        currencies[name] = [soup.find('div', field=field).text for field in fields]
    return currencies


if __name__ == '__main__':
    print(get_currency())
