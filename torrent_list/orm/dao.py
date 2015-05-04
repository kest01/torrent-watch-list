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
    removed_movies = pny.Set('RemovedMovies', lazy=True)
    # movies = pny.Set('Movie', lazy=True)


class Hub(db.Entity):
    url = pny.Required(str)
    module = pny.Required(str)
    description = pny.Optional(str)
    torrents = pny.Set('Torrent')
    users = pny.Set(User)
    removed_movies = pny.Set('RemovedMovies', lazy=True)


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
    removed_movies = pny.Set('RemovedMovies', lazy=True)


class Torrent(db.Entity):
    nnm_id = pny.PrimaryKey(int, size=32)
    title = pny.Required(str)
    torrent_url = pny.Required(str, unique=True)
    url = pny.Required(str, unique=True)
    hub = pny.Required(Hub)
    movie = pny.Optional(lambda: Movie)
    size = pny.Optional(str)
    seeders = pny.Optional(int)
    leechers = pny.Optional(int)
    translation = pny.Optional(str)
    # users = pny.Set(User)


class RemovedMovies(db.Entity):
    movie = pny.Required(Movie)
    hub = pny.Required(Hub)
    user = pny.Required(User)
    pny.PrimaryKey(movie, hub, user)


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


def get_current_user_id():
    # FIXME Mock implementation
    return 1


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
        # add_movie_to_all_users(db_movie)


# def add_movie_to_all_users(movie_id, hub_id):
#     # for u in pny.selects(u for u in User for hub in u.hubs if db_torrent.hub == hub):
#     #     u.torrents.add(db_torrent)
#     for u in pny.selects(u for u in User for hub in u.hubs if hub == hub_id):
#         UserMoviesHub(user=u, hub=hub_id, movie=movie_id)


@pny.db_session
def filter_exist_torrents(url_list):
    ids = {url.split('=')[-1] for url in url_list}
    exist = pny.select(t.url for t in Torrent if t.nnm_id in ids)
    return url_list.difference(exist)


@pny.db_session
def get_all_movies(hub_id):
    user = get_current_user()
    if hub_id:
        movies = pny.select(m for m in Movie
                            for t in m.torrents
                            if t.hub.id == hub_id and m not in user.removed_movies.movie)
    else:
        movies = pny.select(m for m in Movie
                            if m not in user.removed_movies.movie)

    return transform.movies_db_to_json(movies)

# class RemovedMovies(db.Entity):
#     movie = pny.Required(Movie)
#     hub = pny.Required(Hub)
#     pny.PrimaryKey(movie, hub)
#     user = pny.Required(User)

@pny.db_session
def remove_movies_from_user(toRemove):
    user = get_current_user_id()
    for item in toRemove:
        for hub_id in item['hubIds']:
            RemovedMovies(movie=item['id'], hub=hub_id, user=user)


@pny.db_session
def init_data():
    user = User(name='Test Uset', email='kest01@yandex.ru')

    hub = Hub(url='https://nnm-club.me/forum/viewforum.php?f=218', module='nnm_scraping',
              description='NNM: Зарубежные новинки DVDRip')
    # hub2 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=270', module='nnm_scraping', description='NNM: Отечественные новинки DVDRip')
    hub3 = Hub(url='https://nnm-club.me/forum/viewforum.php?f=888', module='nnm_scraping',
               description='NNM: Новинки (3D)')
    # hub4 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=954', module='nnm_scraping', description='NNM: Новинки (HD)')
    # hub5 = Hub(url='http://nnm-club.me/forum/viewforum.php?f=217', module='nnm_scraping', description='NNM: Экранки')

    user.hubs.add(hub)
    # user.hubs.add(hub2)
    user.hubs.add(hub3)
    # user.hubs.add(hub4)
    # user.hubs.add(hub5)


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
