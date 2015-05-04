__author__ = 'Konstantin'

from flask import Flask
import flask.ext.restful as rest
from flask import request
import logging

import torrent_list.orm.dao as dao
import torrent_list.orm.transform as transform

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = rest.Api(app)

dao.init_db()

class Home(rest.Resource):
    def get(self):
        return {'hello': 'world'}


class Movies(rest.Resource):
    def get(self):
        hub_id = int(request.args['hubid']) if 'hubid' in request.args else None
        movies = dao.get_all_movies(hub_id)
        return movies


class Hubs(rest.Resource):
    def get(self):
        return dao.get_habs_and_new()


class RemoveMovies(rest.Resource):
    def post(self):
        toRemove = request.json
        logging.debug("toRemove list: %s", toRemove)
        if toRemove and len(toRemove) > 0:
            dao.remove_movies_from_user(toRemove)


api.add_resource(Home, '/')
api.add_resource(Movies, '/movies/')
# api.add_resource(MovieItem, '/movies/<int:movie_id>')
api.add_resource(RemoveMovies, '/remove/')
api.add_resource(Hubs, '/hubs/')

if __name__ == '__main__':
    app.run(debug=True)
