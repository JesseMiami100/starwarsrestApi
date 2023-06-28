from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    FavoritePeople = db.relationship("FavoritePeople", backref="user", lazy=True)
    FavoritePlanet = db.relationship("FavoritePlanet", backref="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "is_active": self.is_active,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    is_human = db.Column(db.Boolean(), unique=False, nullable=False)
    FavoritePeople = db.relationship("FavoritePeople", backref="parent", lazy=True)
    def __repr__(self):
        return '<People %r>' % self.eye_color

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "is_human": self.is_human, 
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(), unique=False, nullable=False)
    FavoritePlanet = db.relationship("FavoritePlanet", backref="parent", lazy=True)
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain, 
            "gravity": self.gravity,
            # do not serialize the password, its a security breach
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    def __repr__(self):
        return '<FavoritePeople %r>' % self.people_id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    def __repr__(self):
        return '<FavoritePlanet %r>' % self.planets_id

    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }