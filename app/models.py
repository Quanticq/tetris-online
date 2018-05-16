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
    tournament = db.relationship("Tournament", secondary=tournaments_users, back_populates="member")

    def __repr__(self):
        return "<User {}>".format(self.name)


class Tournament(db.Model):
    __tablename__ = "tournaments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    description = db.Column(db.String(1024))
    member = db.relationship("User", secondary=tournaments_users, back_populates="tournament")

    def __repr__(self):
        return "<Tournament {}>".format(self.name)


class Fight(db.Model):
    __tablename__ = "fights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournaments.id"))
    user1_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user2_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user1_score = db.Column(db.Integer, default=0, nullable=False)
    user2_score = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(128), default="friendly", nullable=False)

    def __repr__(self):
        return '<Fight {0} vs. {1}>'.format(self.user1_id, self.user2_id)
