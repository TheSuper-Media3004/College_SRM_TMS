from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(20), unique=True, nullable=False)
    driver_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Bus('{self.bus_number}', '{self.driver_name}')"


class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(10), nullable=False)
    route_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    boarding_points = db.relationship('BoardingPoint', backref='route', lazy=True, cascade="all, delete-orphan")
    students = db.relationship('Student', backref='route', lazy=True)

    def __repr__(self):
        return f"Route('{self.route_number}', '{self.route_name}')"


class BoardingPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop_number = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    pickup_time = db.Column(db.Time, nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    students = db.relationship('Student', backref='boarding_point', lazy=True)

    def __repr__(self):
        return f"BoardingPoint('{self.location}', '{self.pickup_time}')"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    enrollment_number = db.Column(db.String(20), unique=True, nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)
    boarding_point_id = db.Column(db.Integer, db.ForeignKey('boarding_point.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Student('{self.student_name}', '{self.enrollment_number}')"

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='complaints', lazy=True)
    bus = db.relationship('Bus', backref='complaints', lazy=True)

    def __repr__(self):
        return f"Complaint('{self.subject}', '{self.created_at}')"
