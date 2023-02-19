# import json
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self):
        self.book_title = None
        self.mirror_list = []


def search_title(searchterm):
    result = requests.get('http://gen.lib.rus.ec/', params={'req': searchterm})
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
    links_dct = {}
    for search_result in raw_json:
        for mirror in search_result['mirror_list']:
            links_dct[mirror] = None

    actual_links = []

    with ThreadPoolExecutor() as executor:
        for source_link in links_dct.keys():
            actual_links.append(executor.submit(
                get_actual_download_link, source_link))
    result_list = [s_l.result() for s_l in actual_links]
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
    res = requests.get(page_link)
    # import pdb;pdb.set_trace()
    soup = BeautifulSoup(res.text, 'html5lib')
    selector = '#maintable > tbody > tr:nth-child(1) > td:nth-child(2) > a'
    logger.debug(soup.select(selector))
    url_suffix_params = soup.select(selector)[0].get('href')
    return '/'.join(page_link.split('/')[:-1]) + f'/{url_suffix_params}'


if __name__ == '__main__':
    # rj = search_title(searchterm='reilly')
    # print(json.dumps(rj, indent=1))
    link = get_actual_download_link(
        'http://libgen.lc/ads.php?md5=14E1777E94C28EDB7A5B80A1370E4086')
    print(link)
