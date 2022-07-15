#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json

from sqlalchemy import Column, Integer, String
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm

from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String(300))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(
        db.Boolean, default=False, server_default="false")
    seeking_description = db.Column(db.String(255))
    Shows = db.relationship('Shows', backref='Venue',
                            cascade='all,delete-orphan', lazy='dynamic')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

venue=Venue
class Artist(db.Model):
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

artist =Artist
class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    #venue_name =db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
   # artist_name =db.Column(db.String)
    #artist_image_link=db.Column(db.String(255),nullable= False)
    #start_time=db.Column(db.Date, default=datetime.utcnow)
    start_time = db.Column(db.DateTime, nullable=False)


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# for home page route

@app.route('/')
def index():
    return render_template('pages/home.html')


# to return all Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    data = Venue.query.all()
    return render_template('pages/venues.html', areas=data)


# route for implementing search for Venue

@app.route('/venues/search', methods=['POST'])
def search_venues():

    searched = search_term = request.form.get('search_term', '')
    count = Venue.query.filter_by(name=searched).count()
    fetchedData = Venue.query.filter_by(name=searched).all()

    response = {
        "count": count,
        "data": fetchedData
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


# route to get venue by venue_id

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.get_or_404(venue_id)
    return render_template('pages/show_venue.html', venue=data)


# route to bring form for us in browser by using get request

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


# route to create new Venue in database

@app.route('/venues/create', methods=['POST']) 
def create_venue_submission(): 


# to prevent from  UnboundLocalError: local variable 'venue' referenced before assignment we use glabal to use global variable in locally

  global venue
  try:
    form = VenueForm(request.form)
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      image_link=form.image_link.data,
      website=form.website.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data
      )
    db.session.add(venue)
    db.session.commit()

        # flash success when venue successfully submitted or inserted

    flash('Venue: {0} created successfully'.format(venue.name))
    return redirect('/venues')

        # render_template('pages/home.html')
  except Exception as err:
    flash('An error occur creating the Venue: {0}. Error: {1} '.format(
    venue.name, err))
    db.session.rollback()
    return render_template('pages/home.html')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

# block to delete venues

@app.route('/venues/delete/<venue_id>')
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue Data  was successfully Deleted!')
    return redirect('/venues')



# route to get all artist from database

@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)



# artist search route implementation

@app.route('/artists/search', methods=['POST'])
def search_artists():
    searched = search_term = request.form.get('search_term', '')
    count = Artist.query.filter_by(name=searched).count()
    fetchedData = Artist.query.filter_by(name=searched).all()

    response = {
        "count": count,
        "data": fetchedData
    }
    return render_template('pages/search_artists.html', results=response, search_term=searched)


# route to get artist by its ID

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    data = Artist.query.get_or_404(artist_id)
    return render_template('pages/show_artist.html', artist=data)



#  to update any record we must firstly get its ID to update specific record

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)

    # TODO: populate form with fields from artist with ID <artist_id>

    return render_template('forms/edit_artist.html', form=form, artist=artist)

#  after get record id or specific id we are ready to do update here

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    if request.method == 'POST':
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = request.form['genres']
        artist.facebook_link = request.form['facebook_link']
        artist.image_link = request.form['image_link']
        artist.seeking_venue = request.form['seeking_venue']
        artist.seeking_description = request.form['seeking_description']
        db.session.commit()

        flash('Artist Data ' + artist.name + ' was successfully Updated!')
        return redirect('/artists')
    else:
        return redirect(url_for('show_artist', artist_id=artist_id))


# block to delete artists

@app.route('/artists/delete/<artist_id>')
def delete_artist(artist_id):
    # TODO: Complete this endpoint for taking a artist_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    artist = Artist.query.get_or_404(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist Data  was successfully Deleted!')
    return redirect('/artists')

    # else:
    #flash('Artist Data  was failed to be Deleted!')
    # return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    global venue
    venue = Venue.query.get_or_404(venue_id)
    if request.method == 'POST':
      try:
        form = VenueForm(request.form)
        venue.name = form.name.data,
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.website = form.website.data
        venue.facebook_link = form.facebook_link.data
        venue.image_link = form.image_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        db.session.commit()

        # flash success when Venue successfully updated or modified

        flash('Artist {0} have Updated successfully'.format(venue.name))
        return redirect('/venues')
    
        # catch error when update venue failed
      except Exception as err:
        flash('An error occur updating the Venue {0}. Error: {1} '.format(
        venue.name, err))
        db.session.rollback()
        return redirect(url_for('show_venue', venue_id=venue))
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  global artist
  try:
    form = ArtistForm(request.form)
    artist= Artist(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      phone = form.phone.data,
      genres = form.genres.data,
      facebook_link = form.facebook_link.data,
      image_link = form.image_link.data,
      website_link = form.website_link.data,
      seeking_venue = form.seeking_venue.data,
      seeking_description = form.seeking_description.data
      )
    db.session.add(artist)
    db.session.commit()

        # flash success when Artist successfully submitted or inserted

    flash('Artist {0} created successfully'.format(artist.name))
    return redirect('/artists')
    
    # catch error when submit artist failed
  except Exception as err:
    flash('An error occur creating the Artist: {0}. Error: {1} '.format(
    artist.name, err))
    db.session.rollback()
    return render_template('pages/home.html')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  



# to display shows data

@app.route('/shows')
def shows():
    data = db.session.query(Shows, Artist, Venue).join(
        Artist, Shows.artist_id == Artist.id).join(Venue, Shows.venue_id == Venue.id).all()

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():

    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    n_post = Shows(artist_id=artist_id, venue_id=venue_id,
                   start_time=start_time)
    db.session.add(n_post)
    db.session.commit()

    flash('Show was successfully listed!')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == "__main__":
    app.run(debug=True)
