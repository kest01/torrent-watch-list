__author__ = 'Konstantin'

# from .dao import Movie as DbMovie
# from .dao import Torrent as DbTorrent
#
# from torrent_list.scraping.nnm_scraping import Movie as ScMovie
# from torrent_list.scraping.nnm_scraping import Torrent as ScTorrent


def torrent_sc_to_db(t):
    db_torrent = Torrent(nnm_id=t.nnm_id, title=t.title, torrent_url=t.torrent_url, url=t.url)
    db_torrent.size = t.size
    db_torrent.translation = t.translation
    db_torrent.seeders = t.seeders
    db_torrent.leechers = t.leechers

    return db_torrent


def movie_sc_to_db(m):

    db_movie = Movie(description=m.description, full_name=m.full_name, name_rus=m.name_rus, found_date=m.found_date)
    db_movie.name_eng = m.name_eng
    db_movie.actors = m.actors
    db_movie.genre = m.genre
    db_movie.imdb_id = m.imdb_id
    db_movie.kinopoisk_id = m.kinopoisk_id
    db_movie.poster_url = m.poster_url
    db_movie.year = m.year
    db_movie.imdb_rating = m.imdb_rating

    db_movie.torrents.add(torrent_sc_to_db(m.torrent))

    return db_movie


def movies_db_to_json(movies):

    def is_new(movie):
        return True

    def movie_translation(movie):
        result = None
        for torrent in movie.torrents:
            if torrent.translation:
                if 'дубл' in torrent.translation.lower():
                    return torrent.translation
                result = torrent.translation
        return result

    def calc_seeders(movie):
        return sum([t.seeders for t in movie.torrents])

    def calc_leechers(movie):
        return sum([t.leechers for t in movie.torrents])

    return [
        {
            'id': m.id,
            'nameFull': m.full_name,
            'year': m.year,
            'genre': m.genre,
            'description': m.description,
            'actors': m.actors,
            'imdbId': m.imdb_id,
            'imdbRating': m.imdb_rating,
            'posterUrl': m.poster_url,
            'translation': movie_translation(m),
            'seeders': calc_seeders(m),
            'leechers': calc_leechers(m),
            'isNew': is_new(m),
            'favorites': False,
            'torrents': torrents_db_to_json(m)
        }
        for m in movies

    ]

def torrents_db_to_json(movie):
    return [
        {
            'title': t.title,
            'size': t.size,
            'translation': t.translation,
            'url': t.url,
            'seeders': t.seeders,
            'leechers': t.leechers,
            'torrentUrl': t.torrent_url
        }
        for t in movie.torrents
    ]