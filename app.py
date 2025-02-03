import json
import difflib  # for checking similar lines
import requests
import math
from flask import Flask, render_template, request, jsonify

# reading DB-datas from json-file
with open("countries_wineyards.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Earth radius in km
R = 6371.0

# function for calculating distance between coordinates 
def haversine(lat1, lon1, lat2, lon2):
    # Преобразуем градусы в радианы
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Разница координат
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Формула Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Расстояние в километрах
    distance = R * c
    return distance

# checking if a country has wine regions and how many
# country = input("Which country do you plan to travel to? ").strip()
def check_country():   
    if country in data:
        regions = data[country]
        print(f"{country} has {len(regions)} wine regions.")
        info_check = input("Do you want a summary about these regions? (yes/no) ")
        if info_check.lower() == "yes":
            region_info(country)
    # checking if user typed country name wrong
    else:
        suggestions = difflib.get_close_matches(country, data.keys(), n=3)

        if suggestions:
            print(f"There is no such country as {country}. Did you mean ", end="")
            for suggestion in suggestions:
                print(f"{suggestion}? (yes/no) ", end="")
                answer = input("")
                if answer.lower() == "yes":
                    regions = data[suggestion]
                    print(f"{suggestion} has {len(regions)} wine regions.")
                    info_check = input("Do you want a summary about these regions? (yes/no) ")
                    if info_check.lower() == "yes":
                        region_info(suggestion)
                    break
                elif answer.lower() == "no":
                    continue        # checking next suggestion if user says no
                else:
                    print("Invalid answer. Please type 'yes' or 'no'.")
            else:
                print(f"There are no wine regions in {country}.")
        else:
            print(f"There are no wine regions in {country}.")

# shows info about wine regions of a specific country
def region_info(country):
    print(f"Here are the most famous wine regions in {country}:")
    regions = data[country]
    for index, region in enumerate(regions, start=1):
        print(f"{index}. {region["name"]}. {region["features"]}.")

# getting coordinates of a destination city 
def get_city_coordinates(city):
    api_url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key=ec649d59b98544418a266310e1c10ed7"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()  # geting data in json-format
        if data['results']:
            # getting the first result if there is more then 1 city with such a name
            first_result = data['results'][0]
            lat = first_result['geometry']['lat']
            lng = first_result['geometry']['lng']
            return lat, lng
        else:
            print("Coordinates could not be found")
            return None
    else:
        print("Error:", response.status_code)
        return None

# load data about wineries from json
def load_wine_regions(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
      
# searching wineries in 100 km radius from a destination city 
def find_nearby_wine_regions(city, wine_regions):
    city_lat, city_lng = get_city_coordinates(city)
    if city_lat is None or city_lng is None:
        return []

    nearby_regions = []
    for country, regions in wine_regions.items():
        for region in regions:
            if 'coordinates' in region:
                region_lat = region['coordinates'][0]
                region_lng = region['coordinates'][1]
                distance = haversine(city_lat, city_lng, region_lat, region_lng)
                if distance <= 100:
                    
                    region['country'] = country  
                    region['distance'] = distance  
                    nearby_regions.append(region)

    return nearby_regions
    

# check_country()
city = "Nice"
file_path = 'countries_wineyards.json'  # path to json
wine_regions = load_wine_regions(file_path)

nearby_regions = find_nearby_wine_regions(city, wine_regions)

if nearby_regions:
    print(f"Wine regions within 100 km of {city}:")
    for region in nearby_regions:
        print(f"Country: {region['country']}, Name: {region['name']}, Features: {region['features']}, Distance: {region['distance']:.2f} km")
else:
    print(f"No wine regions found within 100 km of {city}.")

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search_regions', methods=['POST'])
def search_regions():
    city = request.form.get('city')
    nearby_regions = find_nearby_wine_regions(city, wine_regions)
    return jsonify(nearby_regions)

@app.route('/country_info', methods=['POST'])
def get_country_info():
    country = request.form.get('country')
    if country in data:
        return jsonify({
            'success': True,
            'regions': data[country],
            'count': len(data[country])
        })
    suggestions = difflib.get_close_matches(country, data.keys(), n=3)
    return jsonify({
        'success': False,
        'suggestions': suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)


