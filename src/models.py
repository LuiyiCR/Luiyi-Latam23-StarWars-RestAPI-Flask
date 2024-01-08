from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    class People(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), nullable=False)
        height = db.Column(db.String(10))
        mass = db.Column(db.String(10))
        hair_color = db.Column(db.String(50))
        skin_color = db.Column(db.String(50))
        eye_color = db.Column(db.String(50))
        birth_year = db.Column(db.String(10))
        gender = db.Column(db.String(20))

        def __repr__(self):
            return '<People %r>' % self.name

        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "height": self.height,
                "mass": self.mass,
                "hair_color": self.hair_color,
                "skin_color": self.skin_color,
                "eye_color": self.eye_color,
                "birth_year": self.birth_year,
                "gender": self.gender,
            }

            #test
