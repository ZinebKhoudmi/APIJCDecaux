import requests
import folium
import time

# Fonction pour récupérer les données de l'API JCDecaux
def get_station_data(api_key, city):
    url = f"https://api.jcdecaux.com/vls/v3/stations?apiKey={api_key}&contract={city}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la récupération des données.")
        return None

# Fonction pour afficher les stations sur une carte
def display_stations_on_map(stations, city):
    map = folium.Map(location=[stations[0]['position']['latitude'], stations[0]['position']['longitude']], zoom_start=13)
    for station in stations:
        folium.Marker([station['position']['latitude'], station['position']['longitude']], 
                      popup=f"{station['name']}<br/>Bikes available: {station['mainStands']['availabilities']['bikes']}",
                      icon=folium.Icon(color='blue')).add_to(map)
    map.save(f"{city}_bike_stations_map.html")
    print(f"La carte des stations de vélo pour la ville de {city} a été sauvegardée.")

# Fonction pour mettre à jour les informations en temps réel
def update_data_in_real_time(api_key, city):
    while True:
        stations = get_station_data(api_key, city)
        if stations:
            display_stations_on_map(stations, city)
        time.sleep(60)  # Attendre une minute avant de rafraîchir les données

# Paramètres
api_key = "38f670c6daa63c1d665f3e718661d027fe86f075"
city = "nancy"  # Vous pouvez choisir une autre ville supportée par l'API JCDecaux

# Exécution
stations = get_station_data(api_key, city)
if stations:
    display_stations_on_map(stations, city)
    update_data_in_real_time(api_key, city)
