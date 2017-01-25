from flask import Flask

from app import app, db
from pprint import pprint


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    score = db.Column(db.Integer)
    current_flag = db.Column(db.String(80))
    next_score = db.Column(db.Integer)

    def __init__(self, username):
        self.username = username
        self.score = 0
        self.current_flag = ""
        self.next_score = 0

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()

    def set_user_score(self, score):
        self.score = score

    def add_score(self, score):
        self.score += score

    def add_user_next_score(self, next_score):
        self.score += next_score
