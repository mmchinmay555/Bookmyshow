from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from .models import RegisteredUser, Theaters, Movie, Show, Ticket
from . import db
import os
import secrets
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    shows = Show.query.all()
    movies = Movie.query.all()
    
    return render_template('home.html', user = current_user, movies = movies)

@views.route('/movies')
@login_required
def movies():
    if current_user.is_super_admin == True:
        return render_template('movies.html', user = current_user)
    return redirect(url_for('views.home'))

@views.route('/add_movies', methods=['GET', 'POST'])
@login_required
def add_movies():
    if current_user.is_super_admin == True:
        if request.method == 'POST':
            movie_title =  request.form.get('title')
            movie_starring = request.form.get('starring')
            movie_production_house = request.form.get('production_house')
            movie_no_of_watched = 0
            print(type(request.files['poster']))
            movie_poster = save_images(request.files['poster'])

            # check if all the fields are not empty
            if len(movie_title) >= 1 and len(movie_starring) >= 1 and len(movie_production_house) >= 1 :
                # good to go
                new_movie = Movie(poster = movie_poster, title = movie_title, starring = movie_starring, production_house = movie_production_house, no_of_watched = movie_no_of_watched, movie_admin_id = current_user.id)

                db.session.add(new_movie)
                db.session.commit()

                flash( movie_title + ' is being added', category='success')
                return redirect(url_for('views.movies'))
            else:
                flash('Make sure all the fields are filled', category='error')
                return render_template('add_movies.html', user = current_user)
        else:
            return render_template('add_movies.html', user = current_user)
    return redirect(url_for('views.home'))


@views.route('/update_movies/<int:id>', methods = ['POST', 'GET'])
@login_required
def update_movies(id):
    if current_user.is_super_admin == True:
        movie_to_update = Movie.query.get(int(id))
        if request.method == 'POST':
            movie_to_update.poster = save_images(request.files['poster'])
            movie_to_update.title =  request.form.get('title')
            movie_to_update.starring = request.form.get('starring')
            movie_to_update.production_house = request.form.get('production_house')
            
            db.session.commit()

            flash( movie_to_update.title + ' updated succesfully', category='success')
            return redirect(url_for('views.movies'))
        else:
            if movie_to_update:
                return render_template('update_movies.html', user = current_user, movie = movie_to_update)
    else:
        return redirect(url_for('movies.home'))



@views.route('/my_theaters')
@login_required
def my_theaters():
    if current_user.is_theatre_admin == True:
        movies = Movie.query.all()
        return render_template('my_theaters.html', user = current_user, movies = movies)
    return redirect(url_for('views.home'))

@views.route('/select_theaters/<int:id>')
def select_theaters(id):
    # movie_id
    shows = Show.query.filter_by(movie_screened = int(id)).all()
    movie = Movie.query.get(int(id))
    print("line 90")
    if shows:
        return render_template('select_theaters.html', user = current_user, shows = shows, movie = movie)
    else :
        flash( 'This movie has no shows currently', category='note')
        return redirect(url_for('views.home'))

@views.route('/add_theaters', methods=['GET', 'POST'])
@login_required
def add_theaters():
    if current_user.is_theatre_admin == True:
        if request.method == 'POST':
            theater_name =  request.form.get('name')
            theater_address = request.form.get('address')
            theater_location = request.form.get('location')
            theater_city = request.form.get('city')
            theater_contact_no = request.form.get('contact_no')

            # check if all the fields are not empty
            if len(theater_name) >= 1 and len(theater_address) >= 1 and len(theater_location) >= 1 and len(theater_city) >= 1 and len(theater_contact_no) == 10:
                # good to go
                new_theater = Theaters(name = theater_name, address = theater_address, location = theater_location, city = theater_city, contact_no = theater_contact_no, theater_admin_id = current_user.id)
                db.session.add(new_theater)
                db.session.commit()

                flash('Your Theater is being added', category='success')
                return redirect(url_for('views.my_theaters'))
            else:
                flash('Make sure all the fields are filled', category='error')
                return render_template('add_theaters.html', user = current_user)
        else:
            return render_template('add_theaters.html', user = current_user)
    return redirect(url_for('views.home'))

@views.route('/my_tickets')
@login_required
def my_tickets():
    return render_template('my_tickets.html', user = current_user)

@views.route('/book_ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def book_ticket(id):
    if current_user.is_super_admin == False and current_user.is_theatre_admin == False:
        show_to_book = Show.query.get(int(id))
        
        if request.method == 'POST':
            theater = Theaters.query.filter_by(name = str(show_to_book.theater)).first()

            print(theater.name)
            ticket_no_of_seats = request.form.get('no_of_seats')
            # update the number of seats
            show_to_book.seats_available = int(show_to_book.seats_available) - int(ticket_no_of_seats)

            new_ticket = Ticket(show_booked = show_to_book.id, movie_booked = show_to_book.movie_screened, theater_booked = show_to_book.theater_screened_in, user = current_user.id, movie_name = show_to_book.movie, theater_name = show_to_book.theater, theater_address = theater.address, theater_address_link = theater.location, no_of_seats = ticket_no_of_seats, total_cost = int(show_to_book.cost_per_seat) * int(ticket_no_of_seats), show_timinig = show_to_book.datetime_screened)
            
            db.session.add(new_ticket)
            db.session.commit()

            flash('Your Show is being added', category='success')
            return redirect(url_for('views.my_tickets'))
        else:
            return render_template('book_ticket.html', user = current_user, show = show_to_book)
    else:
        return redirect(url_for('views.select_theaters'))

@views.route('/add_shows', methods=['GET', 'POST'])
@login_required
def add_shows():
    print('reached 116')
    movies = Movie.query.all()
    theaters = Theaters.query.filter_by(theater_admin_id = int(current_user.id)).all()
    if current_user.is_theatre_admin == True:
        print('reached 120')
        if request.method == 'POST':
            print('reached 122')
            show_movie_screened = Movie.query.filter_by(title = request.form.get('movie_screened')).first().id
            if show_movie_screened:
                show_theater_screened_in = request.form.get('theater_screened_in')
                show_movie = request.form.get('movie_screened')
                show_theater = Theaters.query.filter_by(id = request.form.get('theater_screened_in')).first()
                show_date_time_screened = datetime.strptime(request.form.get('date_time_screened'), '%Y-%m-%dT%H:%M')
                show_seats_available = request.form.get('seats_available')
                show_cost_per_seat = request.form.get('cost_per_seat')
            else:
                flash('Movie doesn\'t exist', category='warning')
                return render_template('add_shows.html', user = current_user, movies = movies, theaters = theaters)
            print(show_movie_screened)

            if show_movie_screened >= 1 and show_theater_screened_in >= 1  and show_seats_available >= 1:
                new_show = Show(movie_screened = show_movie_screened, theater_screened_in = show_theater_screened_in, movie = show_movie, theater = show_theater.name, theater_address = show_theater.address, theater_address_link = show_theater.location, datetime_screened = show_date_time_screened, theater_admin_id = current_user.id, seats_available = show_seats_available, cost_per_seat = show_cost_per_seat)
                db.session.add(new_show)
                db.session.commit()
                flash('Your Show is being added', category='success')
                return redirect(url_for('views.my_theaters'))
            else:
                flash('Make sure all the fields are filled', category='error')
                return render_template('add_shows.html', user = current_user, movies = movies, theaters = theaters)
        else:
            return render_template('add_shows.html', user = current_user, movies = movies)
    else:
        return render_template('home.html', user = current_user, movies = movies)

@views.route('show_tickets/<int:id>')
@login_required
def show_tickets(id):
    if current_user.is_theatre_admin == True:
        tickets = Ticket.query.filter_by(show_booked = int(id)).all()
        show = Show.query.get(int(id))
        return render_template('show_tickets.html', user = current_user, tickets = tickets, show = show, no_of_tickets = len(tickets))
    else:
        return render_template('home.html', user = current_user, movies = movies)
        

def save_images(poster):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(poster.filename)
    image_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/movie_posters', image_name)
    poster.save(file_path)
    return image_name

