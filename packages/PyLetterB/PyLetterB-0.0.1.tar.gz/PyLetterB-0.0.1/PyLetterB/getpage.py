from bs4 import BeautifulSoup
import urllib3


def get_page(url):
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
    url_opener = urllib3.PoolManager(headers=user_agent)
    page = url_opener.request('GET', url)
    soup = BeautifulSoup(page.data, from_encoding='utf-8', features='html.parser')
    return soup

