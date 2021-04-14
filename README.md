# Bookmyshow
Movie Booking System similar to bookmyshow

## Working of the App
We have 3 categories of users

Super Admin
<li> Add movies to the database </li>
<li> Make sure you use email with domain as '@bookmyshow.com' while registering
  
Theater Admin
<li> Register his theater and add shows in his theater </li>
<li> Make sure you check the box for Theater Admin while registering
  
Normal User
<li> Book shows </li>

So basically, Super admin adds movies to the database and theater admin add theaters to the database and update shows for his/her theater and normal user books the show

## Setup and Installation

```bash
git clone <repo-url>
```
## Requirements
```bash
pip install flask
pip install Flask-SQLAlchemy
pip flask-login
```
if you get amy No Module found error, 
```bash
pip install <module name>
```

## Run the app
```bash
python main.py
```
