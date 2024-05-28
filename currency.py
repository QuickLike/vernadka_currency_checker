from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests


def get_currency() -> tuple[str, str]:
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
    currency = (
        soup.find('div', field='tn_text_1680795335003').text,
        soup.find('div', field='tn_text_1680795214553').text
    )
    return currency


if __name__ == '__main__':
    print(get_currency())
