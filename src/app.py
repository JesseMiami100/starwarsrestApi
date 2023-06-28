"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, FavoritePeople, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def eet_all_users():

    response_body = User.query.all()  

    all_users = list(map(lambda item: item.serialize(), response_body))

    return jsonify(all_users), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_favorites(user_id):

    user = User.query.get(user_id)  
    favorites = user.FavoritePeople + user.FavoritePlanet
    all_favorites = list(map(lambda item: item.serialize(), favorites))
    
    return jsonify(all_favorites), 200

@app.route('/people', methods=['GET'])
def get_people():

    response_body = People.query.all()  

    all_people = list(map(lambda person: person.serialize(), response_body))

    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    response_body = People.query.filter_by(id = people_id).first() 
    
    if response_body is None: return jsonify("character not found")
    
    return jsonify(response_body.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    response_body = Planets.query.all()  

    all_planets = list(map(lambda planet: planet.serialize(), response_body))

    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    response_body = Planets.query.filter_by(id = planet_id).first() 
    
    if response_body is None: return jsonify("planet not found")
    
    return jsonify(response_body.serialize()), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    response_body = request.get_json()
    user_id = response_body["user_id"]

    Favorite_Planet = FavoritePlanet(user_id = user_id, planets_id = planet_id)

    db.session.add(Favorite_Planet)
    db.session.commit()
    
    return jsonify("favorite planet has been added"), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    response_body = request.get_json()
    user_id = response_body["user_id"]

    Favorite_People = FavoritePeople(user_id = user_id, people_id = people_id)

    db.session.add(Favorite_People)
    db.session.commit()
    
    return jsonify("favorite people has been added"), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    response_body = request.get_json()
    user_id = response_body["user_id"]

    Favorite_People = FavoritePeople.query.filter_by(people_id=people_id,user_id=user_id).first()

    db.session.delete(Favorite_People)
    db.session.commit()
    
    return jsonify("favorite people has been removed"), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    response_body = request.get_json()
    user_id = response_body["user_id"]

    Favorite_Planets = FavoritePlanet.query.filter_by(planet_id=planet_id,user_id=user_id).first()

    db.session.delete(Favorite_Planets)
    db.session.commit()
    
    return jsonify("favorite planet has been removed"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

