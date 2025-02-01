import requests

# Функция для получения координат города
def get_coordinates(city):
    api_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key=YOUR_API_KEY"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            return lat, lng
        else:
            print("Город не найден.")
            return None
    else:
        print(f"Ошибка: {response.status_code}")
        return None

# Функция для поиска виноделен в радиусе 100 км от координат города
def get_wineries_nearby(lat, lng):
    # Пример API-запроса для поиска виноделен в радиусе 100 км
    api_url = f"https://api.example.com/wineries?lat={lat}&lng={lng}&radius=100"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data
        else:
            print("Винодельни не найдены в радиусе 100 км.")
            return None
    else:
        print(f"Ошибка: {response.status_code}")
        return None

# Asking user about a city
city = input("Введите город: ")

# getting city coordinates
coordinates = get_coordinates(city)
if coordinates:
    lat, lng = coordinates
    # searching for winyards in 100 km radius
    wineries = get_wineries_nearby(lat, lng)
    if wineries:
        print(f"Винодельни в радиусе 100 км от города {city}:")
        for winery in wineries:
            print(winery)