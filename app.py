import requests
from flask import Flask , render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)                # SQLAlchemy for database

class City(db.Model):                   # creating class to store the cities in database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()
    
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&APPID=2862eb79900abf023b5d61bcb96c466d'      # url of ur signed weather api

    weather_data = []
    for city in cities:
        
        r = requests.get(url.format(city.name)).json()               # response in json format
        # json
        temp_in_celsius = r['main']['temp']
        temp_in_celsius = temp_in_celsius - 32
        temp_in_celsius = temp_in_celsius * 5
        temp_in_celsius = temp_in_celsius / 9
        temp_in_celsius = temp_in_celsius - 124
        round(temp_in_celsius,2)
        weather = {
            'city' : city.name,
            'temperature' : temp_in_celsius,
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)
