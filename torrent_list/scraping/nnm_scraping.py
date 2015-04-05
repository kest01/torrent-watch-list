import logging
import datetime
import bs4
import re
from datetime import date
import requests
import torrent_list.utils as utils
from torrent_list.scraping.hub import Movie, Torrent, ParsingException


cookies = {}
#cookies = {'phpbb2mysql_4_sid': '8f45db04b03764d002e8fdceb1444242', 'phpbb2mysql_4_data': 'a%3A2%3A%7Bs%3A11%3A%22autologinid%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22userid%22%3Bs%3A6%3A%22283613%22%3B%7D'}
LOGIN_URL = 'http://nnm-club.me/forum/login.php'
ENCODING = 'windows-1251'

logging.basicConfig(level=logging.DEBUG)

def scrap(url):
    content = get_html_content(url)
    return scrape(content, url)


def get_hub_links(url):
    content = get_html_content(url)
    # logging.info(content)
    soup = bs4.BeautifulSoup(content)

    url_base, _ = utils.split_url(url)

    urls = {url_base + a.attrs.get('href') for a in soup.select(".topictitle a[href^=viewtopic.php]")}

    logging.info(urls)
    return urls


def get_html_content(url):
    if not cookies:
        login()
    logging.info("Getting content of url %s" % url)
    response = requests.get(url, cookies=cookies)

    return response.content.decode(ENCODING)


def login():
    login_info = {'username': 'kest01', 'password': '1q2w3e', 'autologin': 'checked', 'login': 'Вход'}
    rq = requests.post(LOGIN_URL, data=login_info, allow_redirects=False)
    global cookies
    cookies = requests.utils.dict_from_cookiejar(rq.cookies)
    logging.info(cookies)



def scrape(html_content, url):
    try:
        return scrape_torrent(html_content, url)
    except Exception as e:
        logging.error('Error parsing url %s' % url)
        raise e
        # TODO Send Error  message to email

def scrape_torrent(html_content, url):
    movie = Movie()
    torrent = Torrent()
    torrent.url = url
    movie.torrent = torrent

    soup = bs4.BeautifulSoup(html_content)

    if not cheked_by_moderator(soup):
        logging.info(url + ' not checked by moderator')
        return None

    title = soup.find(class_='maintitle').text
    validate(title, "Can't parse title of url %s" % url)
    full_name, year = parse_title(title)
    name_rus, name_eng = get_names(full_name)

    movie.year = year
    movie.full_name = full_name
    movie.name_rus = name_rus
    movie.name_eng = name_eng
    torrent.title = title

    movie.description = get_next_element(soup, ("Описание фильма:", "Описание"))
    movie.genre = get_next_element(soup, ("Жанр:", "Жанры"))
    movie.actors = get_next_element(soup, ("Актеры:", "Актёры:"))

    movie.poster_url = soup.select(".postImgAligned.postImg")[0]['title']
    movie.kinopoisk_id = get_kinopoisk_id(soup)
    movie.imdb_id = get_imdb_id(soup)

    movie.found_date = datetime.datetime.now()

    torrent.size = get_size(soup)
    torrent.translation = get_next_element(soup, ("Перевод:", "Перевод 1:"))
    url_base, _ = utils.split_url(url)
    torrent.torrent_url = url_base + soup.select("a[href^=download.php]")[0]['href']
    torrent.nnm_id = url.split('=')[-1]
    torrent.seeders = get_seeders(soup)
    torrent.leechers = get_leechers(soup)

    return movie


def get_size(soup):
    size = get_next_element(soup, ("Размер:", ))
    size = size.replace('\xa0', ' ')

    return size[0:size.index('(') - 1].strip()


def get_kinopoisk_id(soup):
    digits = re.compile("^[0-9]+$")

    for a in soup.select("a[href*=kinopoisk.ru]"):
        for token in a['href'].split('/'):
            if digits.match(token):
                return token
    return ''


def get_imdb_id(soup):
    digits = re.compile("^tt[0-9]+$")

    for a in soup.select("a[href*=imdb.com]"):
        for token in a['href'].split('/'):
            if digits.match(token):
                return token
    return ''


def get_seeders(soup):
    seed_token = soup.select(".seed")
    if len(seed_token) > 1:
        for s in seed_token[1].text.split():
            if s.isdigit():
                return s
    return 0


def get_leechers(soup):
    leech_token = soup.select(".leech")
    if len(leech_token) > 1:
        for s in leech_token[1].text.split():
            if s.isdigit():
                return s
    return 0

def get_next_element(soup, phrases):
    result = find_phrase(soup, phrases)
    if result:
        element = result.parent.next_sibling
        while element and not get_value(element):
            element = element.next_sibling

        return get_value(element) if element else ''


def get_value(elem):
    if type(elem) is bs4.element.NavigableString:
        return str(elem.string).strip()
    elif type(elem) is bs4.element.Tag:
        return str(elem.text).strip()
    else:
        return str(elem).strip()



def find_phrase(soup, phrases):
    for phrase in phrases:
        result = soup.find(text=re.compile(phrase))
        if result:
            return result


def get_names(full_name):
    delimiter = ' / ' if ' / ' in full_name else '/'
    names = full_name.split(delimiter)

    name_rus, name_eng = names[0], ''
    for index, token in enumerate(names[1:]):
        if is_russian(token.strip()):
            name_rus += delimiter + token
        else:
            name_eng = token
            for token in names[index+2:]:
                name_eng += delimiter + token
            break
    return name_rus, name_eng

def is_russian(str):
    for c in str:
        if 0x400 <= ord(c) < 0x500:
            return True
    return False


def parse_title(title):

    year = full_name = ''

    matches = re.findall("\(\d{4}\)", title)
    if not matches:
        matches = re.findall("\(\s?\d{4}\s?\)", title)
    for m in matches:
        token = int(m[1 : -1])
        if (token > 1900) and (token < date.today().year + 1):
            year = str(token)
            full_name = title[:title.index(m)].strip()
            break
    return full_name, year


def cheked_by_moderator(soup):
    return soup.find(text=re.compile("Оформление проверено модератором"))


def validate(condition, message=''):
    if not condition:
        raise ParsingException(message)


def print_movie(movie):
    from pprint import pprint
    print("Movie:")
    pprint(movie.__dict__)
    print("\nTorrent:")
    pprint(movie.torrent.__dict__)


if __name__ == "__main__":


    URL = 'http://nnm-club.me/forum/viewtopic.php?t=879364'
    # URL = 'http://nnm-club.me/forum/viewtopic.php?t=852125'
    # URL = 'http://nnm-club.me/forum/viewtopic.php?t=882872'

    content = get_html_content(URL)
    movie = scrape_torrent(content, URL)

    if movie:
        print_movie(movie)
    else:
        print("\nreturned None")



