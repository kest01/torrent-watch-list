__author__ = 'Konstantin'

from flask import Flask
import torrent_list.orm.dao as dao
import flask.ext.restful as rest
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = rest.Api(app)

dao.init_db()

class Home(rest.Resource):
    def get(self):
        return {'hello': 'world'}


class Movies(rest.Resource):
    def get(self):
        movies = dao.get_all_movies()
        return movies


class MovieItem(rest.Resource):
    def post(self, movie_id):
        pass


api.add_resource(Home, '/')
api.add_resource(Movies, '/movies/')
api.add_resource(MovieItem, '/movies/<int:movie_id>')

if __name__ == '__main__':
    app.run(debug=True)
