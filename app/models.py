# -*- coding: utf-8 -*-
from app import db


tournaments_users = db.Table(
    "tournaments_users",
    db.Column("tournament_id", db.Integer, db.ForeignKey("tournaments.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    max_score = db.Column(db.Integer, default=0, index=True)
    tournaments = db.relationship("Tournament", secondary=tournaments_users, back_populates="members")

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_score(self, value):
        self.max_score = value


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1024))
    members = db.relationship("User", secondary=tournaments_users, back_populates="tournaments")

    def __repr__(self):
        return "<Tournament {}>".format(self.name)


class Fight(db.Model):
    __tablename__ = "fights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"), default=0)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user1_score = db.Column(db.Integer, default=0, nullable=False)
    user2_score = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(128), default="friendly", nullable=False)

    def __init__(self, u1: User, u2: User, tournament=None, status=None):
        self.user1_id = u1.id
        self.user2_id = u2.id
        if tournament:
            self.tournament_id = tournament.id
        if status:
            self.status = status

    def set_score(self, u: User, value):
        if u.id == self.user1_id:
            self.user1_score = value
        else:
            self.user2_score = value

    def __repr__(self):
        return '<Fight {0} vs. {1}>'.format(self.user1_id, self.user2_id)
