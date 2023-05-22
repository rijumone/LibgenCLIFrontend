# import json
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import requests
from retrying import retry
from bs4 import BeautifulSoup

# MAIN_SEARCH_URL = 'http://gen.lib.rus.ec/'
MAIN_SEARCH_URL = 'https://libgen.is/search.php'

class Book:
    def __init__(self):
        self.book_title = None
        self.mirror_list = []


def check_status(response):
    logger.debug(response.status_code)
    return response.status_code != 200

def check_exc(exception):
    logger.warning(exception)
    return isinstance(exception, requests.exceptions.ConnectionError)

@retry(
    retry_on_exception=check_exc,
    retry_on_result=check_status,
    wrap_exception=True,
    stop_max_attempt_number=3,
    # wait_random_min=500, wait_random_max=1500,
)
def perform_request(searchterm):
    params = {'req': searchterm}
    logger.debug(params)
    return requests.get(MAIN_SEARCH_URL, params=params)


def search_title(searchterm):
    result = perform_request(searchterm)
    # import pdb;pdb.set_trace()
    if result.status_code != 200:
        raise ValueError(f'result.status_code: {result.status_code}')
    source = result.content
    soup = BeautifulSoup(source, 'html5lib')
    table = soup.find('table', class_='c')
    rows = table.find_all('tr')
    # books = []
    raw_json = []

    mirrors = ['Gen.lib.rus.ec', 'Libgen.lc',
               'Z-Library', 'Libgen.pw', 'BookFI.net']

    for row in rows:
        links = row.find_all('a')
        mirrorcount = 0
        book = Book()
        downloads = []
        for link in links:
            title_text = None
            try:
                title = link.attrs['title']
                if title == '':
                    title_text = link.text
                    book.book_title = title_text

                elif title in mirrors:
                    download_link = link.attrs['href']
                    mirrorcount += 1
                    downloads.append(download_link)
                book.mirror_list = downloads
            except KeyError:
                pass
        if book.book_title:
            raw_json.append({'title': book.book_title,
                            'mirror_list': book.mirror_list})
            # books.append(book)

    # fetch actual links via in a multithreaded operation
    # logger.info(raw_json)
    links_dct = {}
    for search_result in raw_json:
        for mirror in search_result['mirror_list']:
            links_dct[mirror] = None
    # logger.debug(links_dct)
    actual_links = []

    with ThreadPoolExecutor() as executor:
        for source_link in links_dct.keys():
            actual_links.append(executor.submit(
                get_actual_download_link, source_link))
    result_list = [s_l.result() for s_l in actual_links]
    result_list = [_ for _ in result_list if _]
    # print(result_list)
    _ctr = 0
    for index, search_result in enumerate(raw_json):
        for mirror in search_result['mirror_list']:
            raw_json[index]['mirror_list'] = result_list[_ctr]
            _ctr += 1
    # print(raw_json)
    return raw_json


def get_actual_download_link(page_link):
    logger.debug(page_link)
    res = requests.get(page_link, allow_redirects=True)
    # import pdb;pdb.set_trace()
    soup = BeautifulSoup(res.text, 'html5lib')
    selector = 'a'
    # logger.debug(soup.select(selector))
    try:
        url_suffix_params = [u.get('href') for u in soup.select(selector) if 'key' in u.get('href')][0]
    except IndexError:
        return None
    return '/'.join(page_link.split('/')[:-1]) + f'/{url_suffix_params}'


if __name__ == '__main__':
    # rj = search_title(searchterm='reilly')
    # print(json.dumps(rj, indent=1))
    link = get_actual_download_link(
        'http://libgen.lc/ads.php?md5=14E1777E94C28EDB7A5B80A1370E4086')
    print(link)
