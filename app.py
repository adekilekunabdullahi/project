#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
import collections
collections.Callable = collections.abc.Callable
from models import db, Artist, Venue, Show 
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
     date = dateutil.parser.parse(value)
  else:
      date =value




  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    state = Venue.query.distinct(Venue.city, Venue.state).all()
    data1 = []
    for city in state:
        location1 = Venue.query.filter_by(state = city.state, city = city.city).all()
        data1.append({
            "name" : city.name,
            "id": city.name,
            "city": city.city,
            "state": city.state,
            "venues": location1})
    
    return render_template('pages/venues.html', areas=data1)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_item = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_item))).all()
  response = {
          "counts": len(result),
           "data": result
           }  
 
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  upcoming_shows = Show.query.join(Artist).filter( Show.venue_id == venue_id).filter(Show.start_time >= current_time).all()

  past_shows = Show.query.join(Artist).filter( Show.venue_id == venue_id).filter(Show.start_time < current_time).all()

  #artist = Artist.query.get(Show.artist_id)
  #or show in                 upcoming_shows.append({
    #            "artist_name": show.artist.name,
     #           "artist_id" : show.artist_id,
      #          "artist_image_link": show.artist.image_link,
          #      "start_time": show.start_time           #     })

#  for show in Show.query.join(Artist).filter( Show.venue_id == venue_id).filter(Show.start_time < current_time).all():
 #        past_shows.append({
  #              "artist_name": show.artist.name,
   #             "artist_id" : show.artist_id,
    #            "artist_image_link": show.artist.image_link,
     #           "start_time": Show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      #          })
  data = {
          "id" : venue.id,
          "name" : venue.name,
          "city" : venue.city,
          "state" : venue.state, 
          "address" : venue.address,
          "phone" : venue.phone,
          "facebook_link" : venue.facebook_link,
          "genres" : venue.genres,
          "seeking_talent" : venue.seeking_talent,
          "image_link" : venue.image_link,
          "seeking_description" : venue.seeking_description,
          "website" : venue.website,
          "past_shows" : past_shows,
          "upcoming_shows" : upcoming_shows,
          "past_shows_count" : len(past_shows),
          "upcoming_shows_count": len(upcoming_shows)
        }
#  data["past_shows"] = past_shows
#  data["upcoming_shows"] = upcoming_shows
 # data["past_shows_count"] = past_shows.count()
  #data["upcoming_shows_count"] = upcoming_shows.count()

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    error = False
    try:
      venue = Venue(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      phone = form.phone.data,
      address = form.address.data,
      genres = ' '.join(form.genres.data),
      website_link= form.website_link.data,
      facebook_link = form.facebook_link.data,
      seeking_talent = form.seeking_talent.data,
      image_link = form.image_link.data,
      seeking_description = form.seeking_description.data
      )
      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + request.form.get('name') + ' could not be created,')
    finally:
      db.session.close()
    if not error: 
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

  # on successful db insert, flash success
   # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE','GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    particular_venue = Venue.query.get(venue_id)
    db.session.delete(particular_venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data1 = Artist.query.all()

  return render_template('pages/artists.html', artists=data1)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_item = request.form.get('search_term', '')
  result = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_item))).all()
  response = {
          "counts": len(result),
           "data": result
           }  
 

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  past_shows = Show.query.join(Venue).filter(Show.artist_id == artist_id, Show.start_time < format_datetime(str(datetime.now()))).all()
  upcoming_shows = Show.query.join(Venue).filter(Show.artist_id == artist_id, Show.start_time > format_datetime(str(datetime.now()))).all()              
  data = {
          "id" : artist.id,
          "name" : artist.name,
          "city" : artist.city,
          "genres" : artist.genres,
          "phone" : artist.phone,
          "website_link" : artist.website,
          "facebook_link" : artist.facebook_link,
          "seeking_venue" : artist.seeking_venue,
          "seeking_description": artist.seeking_description,
          "phone" : artist.phone,
          "state" : artist.state,
          "image_link" : artist.image_link,
          "past_shows" : past_shows,
          "past_shows_count" : len(past_shows),
          "upcoming_shows_count" : len(upcoming_shows),
          "upcoming_shows" : upcoming_shows
          }
   
              # past_shows.append({
               # "venue_name" : show.venue.name,
                #"venue_id": show.venue_id,
               # "venue_image_link": show.venue.image_link,
                #"start_time": show.start_time.}),
   #for show in Show.query.join(Venue, Venue.id == Show.venue_id).filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).all():
   #            upcoming_show.append({
    #            "venue_name":show.venue.name,
     #           "venue_id": show.venue_id,
      #          "venue_image_link": show.venue.image_link,
       #         "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')}),
  #data["pash_shows"] = past_shows
  #data["upcoming_shows"] = upcoming_shows
  #data["upcoming_shows_count"] = len(upcoming_shows)
  #data["past_shows_count"] = len(past_shows)
        
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  particular_artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form)
  error = False
  try:
     artist= particular_artist(
          id = form.id.data,
          name = form.name.data,
          genres = form.genres.data,
          state = form.state.data,
          seeking_venue = form.seeking_venue.data,
          seeking_description = form.seeking_description.data,
          phone = form.phone.data,
          website= form.website_link.data,
          image_link = form.image_link.data,
          city = form.city.data
          )
     db.session.add(artist)
     db.session.commit()
  except:
     db.session.rollback()
     error = True
     print(sys.exc_info())
  finally:
     db.session.close()

  return redirect(url_for('show_artist', artist_id=artist))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  venue1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  particular_venue = Venue.query.get(venue_id)
  error = False
  try:
     venue = particular_venue(
          id = form.id.data,
          name = form.name.data,
          genres = form.genres.data,
          state = form.state.data,
          seeking_talent = form.seeking_venue.data,
          seeking_description = form.seeking_description.data,
          phone = form.phone.data,
          website = form.website_link.data,
          image_link = form.image_link.data,
          city = form.city.data
          )
     db.session.add(venue)
     db.session.commit()
  except:
     db.session.rollback()
     error = True
     print(sys.exc_info())
  finally:
     db.session.close()


  return redirect(url_for('show_venue', venue_id=venue))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  error = False
  
  try:
      artist = Artist(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      phone = form.phone.data,
      genres = ' '.join(form.genres.data),
      facebook_link = form.facebook_link.data,
      seeking_venue = form.seeking_venue.data,
      website = form.website_link.data,
      image_link = form.image_link.data,
      seeking_description = form.seeking_description.data
      )
      db.session.add(artist)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if not error: 
  # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + request.form.get('name') + ' could not be created,')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data1 = []
  Shows = Show.query.all()
  for list_of_show in Shows:
      artist = Artist.query.get(list_of_show.artist_id)
      venue = Venue.query.get(list_of_show.venue_id)
      if list_of_show.start_time > datetime.now():
         data1.append({
        "venue_id" : list_of_show.venue_id,
        "venue_name" : venue.name,
        "artist_id" : list_of_show.artist_id,
        "artist_name" : artist.name,
        "artist_image_link" : artist.image_link,
        "start_time" : list_of_show.start_time 
        })

  return render_template('pages/shows.html', shows=data1)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  error = False
  try:
          show = Show(venue_id = form.venue_id.data,
          artist_id = form.artist_id.data,
          start_time = form.start_time.data)
          db.session.add(show)
          db.session.commit()
  except:
          db.session.rollback()
          print(sys.exc_info())
  finally:
          db.session.close()
  if not error:
          flash('Show was successfully listed!')
  else:
        flash('An error occured, Show could not be listed.')
        

# on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
