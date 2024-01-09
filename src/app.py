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
from models import db, User, People, Planet, Favorites

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


# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if users:
        serialize_users = [user.serialize() for user in users]
        return jsonify(serialize_users), 200
    else:
        return jsonify({"error": "Users not found"}), 404

# Endpoint to get a single user by ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        serialize_user = user.serialize()
        return jsonify(serialize_user), 200
    else:
        return jsonify({"error": "User not fount"}), 404


# Endpoint to get all people
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

# Endpoint to get a sinle person by ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        serialized_person = person.serialize()
        return jsonify(serialized_person), 200
    else:
        return jsonify({"error": "Person not found"}), 404
    
# Endpoint to get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200

# Endpoint to get a single planet by ID
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        serialized_planet = planet.serialize()
        return jsonify(serialized_planet), 200
    else:
        return jsonify({"error": "Planet not found"}), 404
    
# Endpoint to get all favorites that belong to a user
@app.route('/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    serialized_favorite = [favorite.serialize() for favorite in favorites]
    if favorites:
        return jsonify(serialized_favorite), 200
    else:
        return jsonify({"error": "Favorites not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
