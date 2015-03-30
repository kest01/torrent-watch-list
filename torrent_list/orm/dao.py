__author__ = 'KKharitonov'

import pony.orm as pny
import datetime

clear_db_on_startup = False
sql_debug_flag = True

db = pny.Database()


class Torrent(db.Entity):
    nnm_id = pny.PrimaryKey(int, size=32)
    title = pny.Required(str)
    torrent_url = pny.Required(str, unique=True)
    url = pny.Required(str, unique=True)
    movie = pny.Optional(lambda: Movie)
    size = pny.Optional(str)
    translation = pny.Optional(str)


class Movie(db.Entity):
    description = pny.Required(str)
    found_date = pny.Required(datetime.datetime)
    full_name = pny.Required(str)
    name_rus = pny.Required(str)
    name_eng = pny.Optional(str)
    actors = pny.Optional(str)
    genre = pny.Optional(str)
    imdb_id = pny.Optional(str)
    kinopoisk_id = pny.Optional(str)
    poster_url = pny.Optional(str)
    year = pny.Optional(str)
    torrents = pny.Set(Torrent)

def init_db():
    if sql_debug_flag:
        pny.sql_debug(True)

    db.bind("sqlite", "torrents.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
    if clear_db_on_startup:
        db.drop_all_tables(with_all_data=True)
        db.create_tables()

@pny.db_session
def save_movie(movie):
    movies = Movie.select(lambda m: ((movie.imdb_id and m.imdb_id == movie.imdb_id) or (movie.kinopoisk_id and m.kinopoisk_id == movie.kinopoisk_id)))
    # fixme
    convert_movie(movie)

@pny.db_session
def filter_exist_torrents(url_list):
    ids = {url.split('=')[-1] for url in url_list}
    exist = pny.select(t.url for t in Torrent if t.nnm_id in ids)
    return url_list.difference(exist)

def convert_torrent(t):
    db_torrent = Torrent(nnm_id=t.nnm_id, title=t.title, torrent_url=t.torrent_url, url=t.url)
    if t.size:
        db_torrent.size = t.size
    if t.translation:
        db_torrent.translation = t.translation

    return db_torrent


def convert_movie(m):

    db_movie = Movie(description=m.description, full_name=m.full_name, name_rus=m.name_rus, found_date=m.found_date)
    if m.name_eng:
        db_movie.name_eng = m.name_eng
    if m.actors:
        db_movie.actors = m.actors
    if m.genre:
        db_movie.genre = m.genre
    if m.imdb_id:
        db_movie.imdb_id = m.imdb_id
    if m.kinopoisk_id:
        db_movie.kinopoisk_id = m.kinopoisk_id
    if m.poster_url:
        db_movie.poster_url = m.poster_url
    if m.year:
        db_movie.year = m.year

    for t in m.torrents:
        db_movie.torrents.add(convert_torrent(t))

    return db_movie

init_db()

if __name__ == "__main__":
    # @db_session
    def testDB():
        # UserSettings(name='UserName', email='test email')
        # UserSettings(name='UserName2', email='email')
        print("ready to commit")

    init_db()

    testDB()