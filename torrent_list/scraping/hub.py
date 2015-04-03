__author__ = 'Konstantin'

import logging
import requests
# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
import xml.etree.ElementTree as ET

import torrent_list.orm.dao as dao


logging.basicConfig(level=logging.DEBUG)


class Movie:
    pass


class Torrent:
    pass


class DynamicInfo:
    pass


class ParsingException(Exception):
    pass


def scrap_hub(hub):
    module = __import__("torrent_list.scraping.%s" % hub.module, fromlist=[''])
    torrent_links = module.get_hub_links(hub.url)
    torrent_links = dao.filter_exist_torrents(torrent_links)
    for link in torrent_links:
        logging.info("Scraping url %s" % link)
        movie = module.scrap(link)
        if movie:
            fill_ratings(movie)
            dao.save_movie(hub.id, movie)
        else:
            logging.error("\nReturned None for url %s" % hub.url)


def scrap_hubs():
    hubs = dao.get_hubs()

    for hub in hubs:
        scrap_hub(hub)


def fill_ratings(movie):
    if movie.kinopoisk_id:
        movie.kinopoisk_rating, movie.imdb_rating = get_kinopoisk_rating(movie.kinopoisk_id)
        pass
    elif movie.imdb_id:
        movie.kinopoisk_rating, movie.imdb_rating = None, get_imdb_rating(movie.imdb_id)
    else:
        movie.kinopoisk_rating = movie.imdb_rating = None

def get_kinopoisk_rating(kp_id):
    response = requests.get("http://rating.kinopoisk.ru/%s.xml" % kp_id)
    tree = ET.fromstring(response.content)
    kinopoisk_rating = tree.find("kp_rating").text
    imdb_element = tree.find("imdb_rating")
    imdb_rating = imdb_element.text if imdb_element is not None else None

    return kinopoisk_rating, imdb_rating


def get_imdb_rating(imdb_id):
    if imdb_id:
        # response = requests.get("http://www.omdbapi.com/?plot=short&r=json&i=" + imdb_id)
        # return response.json()["imdbRating"]
        response = requests.get("http://app.imdb.com/title/maindetails?tconst=" + imdb_id)
        return response.json()["data"]["rating"]


# ---- TESTS -------------

if __name__ == "__main__":
    dao.clear_db_on_startup = True
    dao.init_db()

    # with dao.pny.db_session:
    #     hub = dao.Hub[2]
    #     scrap_hub(hub)

    scrap_hubs()
    # scrap_hub('nnm_scraping', 'http://nnm-club.me/forum/viewforum.php?f=218')

    # print(get_kinopoisk_rating(770973))
    # print(get_kinopoisk_rating(893371))