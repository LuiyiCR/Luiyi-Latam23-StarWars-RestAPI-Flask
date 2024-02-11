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
from flask import jsonify

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
        return jsonify({"error": "User not found"}), 404


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
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    favorites = Favorites.query.filter_by(user_id=user_id)
    serialized_favorite = [favorite.serialize() for favorite in favorites]
    return jsonify(serialized_favorite), 200

# Endpoint to add a favorite planet to a user
@app.route('/favorites/planet/<int:user_id>', methods=['POST'])
def add_favorite_planet(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        planet_data = request.json
        planet_id = planet_data.get("planet_id")

        if not planet_id:
            return jsonify({"error": "Planet ID is required"}, 400)
        
        planet = Planet.query.get(planet_id)

        if not planet:
            return jsonify({"error": "Planet not found"}), 404
        
        existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()

        if existing_favorite:
            return jsonify({"error": "Planet already in favorites"}), 400
        
        new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"message": "Planet added to favorites"}), 200

    except Exception as e:
     return jsonify({"error": str(e)}), 500

# Endpoint to add a favorite person to a user
@app.route('/favorites/people/<int:user_id>', methods=['POST'])
def add_favorite_person(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        person_data = request.json
        person_id = person.get("person_id")

        if not person_id:
            return jsonify({'error': 'Person ID is required'}), 400
        
        person = People.query.get(person_id)

        if not person:
            return jsonify({'error': 'Person not found'}), 404

        existing_favorite = Favorites.query.filter_by(user_id=user_id, people_id=person_id).first()

        if existing_favorite:
            return jsonify({"error": "Person already in favorites"}), 400
        
        new_favorite = Favorites(user_id=user_id, people_id=person_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({"message": "Person added to favorites"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Function to get a favorite planet by ID
def get_favorite_planet_by_id(planet_id):
    favorite_planet = Favorites.query.filter_by(planet_id=planet_id).first()
    return favorite_planet

# Function to delete a favorite planet with the given ID for a specific user
@app.route('/favorites/planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite_planet = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_planet:
        db.session.delete(favorite_planet)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted"}), 200
    else:
      return jsonify({"error": "Favorite planet not found for this user"}), 404

#Function to get a favorite person with the given ID
def get_favorite_person_by_id(people_id):
    favorite_person = Favorites.query.filter_by(people_id=people_id).first()
    return favorite_person

# Function to delete a favorite person with the given ID for a specific user
@app.route('/favorites/people/<int:user_id>/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(user_id, people_id):
    favorite_person = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite_person:
        db.session.delete(favorite_person)
        db.session.commit()
        return jsonify({"message": "Favorite person deleted"}), 200
    else:
        return jsonify({"error": "Favorite person not found for this user"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
