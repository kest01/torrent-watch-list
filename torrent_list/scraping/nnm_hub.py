__author__ = 'Konstantin'

import requests, logging, bs4
import torrent_list.scraping.nnm_scraping as scraping
import torrent_list.utils as utils
import torrent_list.orm.dao as dao


cookies = {}
#cookies = {'phpbb2mysql_4_sid': '8f45db04b03764d002e8fdceb1444242', 'phpbb2mysql_4_data': 'a%3A2%3A%7Bs%3A11%3A%22autologinid%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22userid%22%3Bs%3A6%3A%22283613%22%3B%7D'}
LOGIN_URL = 'http://nnm-club.me/forum/login.php'
IMDB_API_URL = "http://www.omdbapi.com/?plot=short&r=json&i="
ENCODING = 'windows-1251'

logging.basicConfig(level=logging.INFO)


def scrap_hub(url):
    torrent_links = get_hub_links(url)
    torrent_links = dao.filter_exist_torrents(torrent_links)

    for link in torrent_links:
        content = get_html_content(link)
        movie = scraping.scrape(content, link)
        if movie:
            movie.imdb_rating = get_imdb_rating(movie.imdb_id)
            dao.save_movie(movie)
        else:
            logging.error("\nReturned None for url %s" % url )


def get_hub_links(url):
    content = get_html_content(url)
    # logging.info(content)
    soup = bs4.BeautifulSoup(content)

    url_base, _ = utils.split_url(url)

    urls = {url_base + a.attrs.get('href') for a in soup.select(".topictitle a[href^=viewtopic.php]")}

    logging.info(urls)
    return urls


def get_imdb_rating(imdb_id):
    if imdb_id:
        # response = requests.get("http://www.omdbapi.com/?plot=short&r=json&i=" + imdb_id)
        # return response.json()["imdbRating"]
        response = requests.get("http://app.imdb.com/title/maindetails?tconst=" + imdb_id)
        return response.json()["data"]["rating"]


def get_html_content(url):
    if not cookies:
        login()
    response = requests.get(url, cookies=cookies)

    return response.content.decode(ENCODING)



def login():
    login_info = {'username': 'kest01', 'password': '1q2w3e', 'autologin': 'checked', 'login': 'Вход'}
    rq = requests.post(LOGIN_URL, data=login_info, allow_redirects=False)
    global cookies
    cookies = requests.utils.dict_from_cookiejar(rq.cookies)
    logging.info(cookies)



# ---- TESTS -------------

if __name__ == "__main__":
    dao.init_db()
    scrap_hub('http://nnm-club.me/forum/viewforum.php?f=218')

