__author__ = 'KKharitonov'

import datetime
import logging

import pony.orm as pny
import torrent_list.orm.transform as transform


logging.basicConfig(level=logging.INFO)

clear_db_on_startup = False
sql_debug_flag = True

db = pny.Database()


class User(db.Entity):
    name = pny.Required(str)
    email = pny.Required(str)
    hubs = pny.Set('Hub')
    torrents = pny.Set('Torrent', lazy=True)


class Hub(db.Entity):
    url = pny.Required(str)
    module = pny.Required(str)
    description = pny.Optional(str)
    torrents = pny.Set('Torrent')
    users = pny.Set(User)


class Movie(db.Entity):
    description = pny.Required(str)
    found_date = pny.Required(datetime.datetime)
    full_name = pny.Required(str)
    name_rus = pny.Required(str)
    name_eng = pny.Optional(str)
    actors = pny.Optional(str)
    genre = pny.Optional(str)
    imdb_id = pny.Optional(str)
    imdb_rating = pny.Optional(float)
    kinopoisk_id = pny.Optional(str)
    kinopoisk_rating = pny.Optional(str)
    poster_url = pny.Optional(str)
    year = pny.Optional(str)
    torrents = pny.Set('Torrent')


class Torrent(db.Entity):
    nnm_id = pny.PrimaryKey(int, size=32)
    title = pny.Required(str)
    torrent_url = pny.Required(str, unique=True)
    url = pny.Required(str, unique=True)
    hub = pny.Required('Hub')
    movie = pny.Optional(lambda: Movie)
    size = pny.Optional(str)
    seeders = pny.Optional(int)
    leechers = pny.Optional(int)
    translation = pny.Optional(str)
    users = pny.Set(User)


def init_db():
    if sql_debug_flag:
        pny.sql_debug(True)

    db.bind("sqlite", "torrents.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
    if clear_db_on_startup:
        db.drop_all_tables(with_all_data=True)
        db.create_tables()
        init_data()


@pny.db_session
def get_current_user():
    # FIXME Mock implementation
    return User[1]


@pny.db_session
def save_movie(hub_id, movie):
    query = "SELECT * FROM Movie WHERE full_name = $movie.full_name"
    if movie.imdb_id:
        query += " OR imdb_id = $movie.imdb_id"
    if movie.kinopoisk_id:
        query += " OR kinopoisk_id = $movie.kinopoisk_id"
    db_movie = Movie.get_by_sql(query)
    if db_movie:
        logging.info("Movie already exist in DB. Add new torrent to movie")
        db_torrent = transform.torrent_sc_to_db(movie.torrent, hub_id)
        db_movie.torrents.add(db_torrent)
    else:
        db_movie, db_torrent = transform.movie_sc_to_db(movie, hub_id)
    add_torrent_to_user(db_torrent)


def add_torrent_to_user(db_torrent):
    for u in pny.select(u for u in User for hub in u.hubs if db_torrent.hub == hub):
        u.torrents.add(db_torrent)


@pny.db_session
def filter_exist_torrents(url_list):
    ids = {url.split('=')[-1] for url in url_list}
    exist = pny.select(t.url for t in Torrent if t.nnm_id in ids)
    return url_list.difference(exist)


@pny.db_session
def get_all_movies(hub_id):
    user = get_current_user()
    if hub_id:
        movies = pny.select(m for m in Movie for t in m.torrents for u in t.users if t.hub.id == hub_id and u == user)
    else:
        movies = pny.select(m for m in Movie for t in m.torrents for u in t.users if u == user)

    return transform.movies_db_to_json(movies)


@pny.db_session
def init_data():
    user = User(name='Test Uset', email='kest01@yandex.ru')

    hub = Hub(url='http://nnm-club.me/forum/viewforum.php?f=218', module='nnm_scraping', description='NNM: Зарубежные новинки DVDRip')
    hub2 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=270', module='nnm_scraping', description='NNM: Отечественные новинки DVDRip')
    hub3 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=888', module='nnm_scraping', description='NNM: Новинки (3D)')
    hub4 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=954', module='nnm_scraping', description='NNM: Новинки (HD)')
    hub5 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=217', module='nnm_scraping', description='NNM: Экранки')

    user.hubs.add(hub)
    user.hubs.add(hub2)
    user.hubs.add(hub3)
    user.hubs.add(hub4)
    user.hubs.add(hub5)


@pny.db_session
def get_hubs():
    hubs = Hub.select()
    return hubs[:]

def get_habs_and_new():
    return transform.hubs_db_to_json(get_hubs())

if __name__ == "__main__":
    # @db_session

    clear_db_on_startup = True

    init_db()
