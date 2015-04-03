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
        hub_id = request.args['hubid'] if 'hubid' in request.args else None
        movies = dao.get_all_movies(hub_id)
        return movies


class MovieItem(rest.Resource):
    def post(self, movie_id):
        pass


class Hubs(rest.Resource):
    def get(self):
        return dao.get_habs_and_new()


api.add_resource(Home, '/')
api.add_resource(Movies, '/movies/')
api.add_resource(MovieItem, '/movies/<int:movie_id>')
api.add_resource(Hubs, '/hubs/')

if __name__ == '__main__':
    app.run(debug=True)
