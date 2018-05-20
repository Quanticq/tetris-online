# -*- coding: utf-8 -*-
from random import shuffle

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

tournaments_users = db.Table(
    "tournaments_users",
    db.Column("tournament_id", db.Integer, db.ForeignKey("tournaments.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True)
)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    max_score = db.Column(db.Integer, default=0, index=True)
    tournaments = db.relationship("Tournament", secondary=tournaments_users, back_populates="members", lazy="dynamic")

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_score(self, value):
        if value > self.max_score:
            self.max_score = value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_top_users(count):
        return User.query.order_by(User.max_score.desc())[:count]


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1024))
    members = db.relationship("User", secondary=tournaments_users, back_populates="tournaments", lazy="dynamic")
    fights = db.relationship("Fight", back_populates="tournament", lazy="dynamic")

    def __init__(self, name, description=None):
        self.name = name
        if description:
            self.description = description

    def __repr__(self):
        return "<Tournament {}>".format(self.name)

    def add_member(self, user):
        self.members.append(user)

    def delete_member(self, user):
        self.members.remove(user)

    def create_fights(self):
        status = "1/{0}".format(len(self.members[::2]))
        us1 = self.members[::2]
        us2 = self.members[1::2]
        shuffle(us1), shuffle(us2)

        for pair in list(zip(us1, us2)):
            self.fights.append(Fight(pair[0], pair[1], self.id, status))

    def delete_losers(self):
        status = "1/{0}".format(len(self.members) // 2)
        last_fights = self.fights.filer_by(status=status).all()
        for fight in last_fights:
            self.members.remove(fight.get_looser())


class Fight(db.Model):
    __tablename__ = "fights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), default=0)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user1_score = db.Column(db.Integer, default=0, nullable=False)
    user2_score = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(128), default="friendly", nullable=False)
    tournament = db.relationship("Tournament", back_populates="fights")

    def __init__(self, user1, user2, tournament_id=0, status=None):
        self.user1_id = user1.id
        self.user2_id = user2.id
        if tournament_id:
            self.tournament_id = tournament_id
        if status:
            self.status = status

    def __repr__(self):
        return '<Fight {0} vs. {1}>'.format(self.user1_id, self.user2_id)

    def set_score(self, user, value):
        if user.id == self.user1_id:
            self.user1_score = value
        else:
            self.user2_score = value

    def get_looser(self):
        if self.user1_score > self.user2_score:
            return User.query.get(self.user2_id)
        else:
            return User.query.get(self.user1_id)

    def get_winner(self):
        if self.user1_score > self.user2_score:
            return User.query.get(self.user1_id)
        else:
            return User.query.get(self.user2_id)
