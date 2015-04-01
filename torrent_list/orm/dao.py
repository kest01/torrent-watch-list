__author__ = 'KKharitonov'

import pony.orm as pny
import datetime, logging

import torrent_list.orm.transform as transform

logging.basicConfig(level=logging.INFO)

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
    seeders = pny.Optional(int)
    leechers = pny.Optional(int)
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
    imdb_rating = pny.Optional(float)
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
    query = "SELECT * FROM Movie WHERE full_name = $movie.full_name"
    if movie.imdb_id:
        query += " OR imdb_id = $movie.imdb_id"
    if movie.kinopoisk_id:
        query += " OR kinopoisk_id = $movie.kinopoisk_id"
    db_movie = Movie.get_by_sql(query)
    if db_movie:
        logging.info("Movie already exist in DB. Add new torrent to movie")
        db_movie.torrents.add(transform.torrent_sc_to_db(movie.torrent))
    else:
        transform.movie_sc_to_db(movie)

@pny.db_session
def filter_exist_torrents(url_list):
    ids = {url.split('=')[-1] for url in url_list}
    exist = pny.select(t.url for t in Torrent if t.nnm_id in ids)
    return url_list.difference(exist)


@pny.db_session
def get_all_movies():
    return transform.movie_db_to_json(Movie.select())


# init_db()

if __name__ == "__main__":
    # @db_session
    def testDB():
        # UserSettings(name='UserName', email='test email')
        # UserSettings(name='UserName2', email='email')
        print("ready to commit")

    init_db()

    testDB()