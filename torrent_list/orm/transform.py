__author__ = 'Konstantin'

# from torrent_list.scraping.nnm_scraping import Movie as ScMovie
# from torrent_list.scraping.nnm_scraping import Torrent as ScTorrent


def torrent_sc_to_db(t, hub_id):
    from .dao import Torrent

    db_torrent = Torrent(nnm_id=t.nnm_id, title=t.title, torrent_url=t.torrent_url, url=t.url, hub=hub_id)
    copy_attr(t, db_torrent, ('size', 'translation', 'seeders', 'leechers'))

    return db_torrent


def movie_sc_to_db(m, hub_id):
    from .dao import Movie

    db_movie = Movie(description=m.description, full_name=m.full_name, name_rus=m.name_rus, found_date=m.found_date)
    copy_attr(m, db_movie, ('name_eng', 'actors', 'genre', 'imdb_id', 'kinopoisk_id', 'poster_url', 'year', 'imdb_rating', 'kinopoisk_rating'))
    db_torrent = torrent_sc_to_db(m.torrent, hub_id)
    db_movie.torrents.add(db_torrent)

    return db_movie, db_torrent



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

    def get_rating(movie):
        return movie.imdb_rating if movie.imdb_rating else movie.kinopoisk_rating

    return [
        {
            'id': m.id,
            'nameFull': m.full_name,
            'year': m.year,
            'genre': m.genre,
            'description': m.description,
            'actors': m.actors,
            'imdbId': m.imdb_id,
            'kinopoiskId': m.kinopoisk_id,
            'rating': get_rating(m),
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
            'torrentUrl': t.torrent_url,
            'hub': t.hub.description
        }
        for t in movie.torrents
    ]


def hubs_db_to_json(hubs):
    return [
        {
            'id': h.id,
            'description': h.description,
            'new': h.id - 1,
        }
        for h in hubs
    ]


def copy_attr(source, dest, attr):
    if isinstance(attr, (list, tuple)):
        for a in attr:
            copy_attr(source, dest, a)
    else:
        val = getattr(source, attr)
        if val is not None:
            setattr(dest, attr, val)
