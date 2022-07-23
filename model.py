
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from config import get_config_file




db=SQLAlchemy()
config=dict()

#--------------------------------to get configuration file------------

config=get_config_file()
migrate = Migrate()



class FyyurSession():
    def add(self) -> None:
        db.session.add(self)

    def delete(self) -> None:
        db.session.delete(self)

    def flush(self) -> None:
        db.session.flush()

    def commit() -> None:
        db.session.commit()

    def refresh(self) -> None:
        db.session.refresh()


    def rollback() -> None:
        db.session.rollback()

    def close(self) -> None:
        db.session.close()

class Venue(db.Model,FyyurSession):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    genres = db.Column(db.String(300))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), unique= True)
    seeking_talent = db.Column(
        db.Boolean, default=False, server_default="false")
    seeking_description = db.Column(db.String(255))
    Shows = db.relationship('Shows', backref='Venue',
                            cascade='all,delete-orphan', lazy='dynamic')

    def format(self) -> dict:
        return {'id':self.id, 'name': self.name, 'shows':[shows.format() for shows in self.Shows]}

    

    def __repr__(self) -> str:
        return f'{self.id} - {self.name}'





class Artist(db.Model, FyyurSession):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(200))
    seeking_venue = db.Column(db.String(200))
    seeking_description = db.Column(db.String(255))
    Shows = db.relationship('Shows', backref='Artist',
                            cascade='all,delete-orphan', lazy='dynamic')
    

    def format(self) -> dict:
        return {'id':self.id, 'name': self.name, 'shows':[shows.format() for shows in self.Shows]}

    
    def __repr__(self) -> str:
        return f'{ self.id } - { self.name }'



class Shows(db.Model, FyyurSession):
    __tablename__= 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
    
    start_time = db.Column(db.DateTime, nullable=False)




