# Bookmyshow
Movie Booking System similar to bookmyshow

<img src="https://github.com/mmchinmay555/Bookmyshow/blob/master/Screenshot%20from%202021-04-14%2016-37-31.png"/>

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

------------------------------------------------------------------------------------

So basically, 
<li> Super admin adds movies to the database </li>
<li> theater admin add theaters to the database and update shows for his/her theater </li>
<li> normal user books the show </li>

## Setup and Installation

```bash
git clone <repo-url>
```
## Requirements
```bash
pip install flask
pip install Flask-SQLAlchemy
pip install flask-login
```
if you get any No Module found error, 
```bash
pip install <module name>
```

## Run the app
```bash
python main.py
```
