import sqlite3
import cartopy.crs as ccrs
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy

class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path, cities, marker_color='red'):
        if not cities:
            return None

        # Создаем карту
        fig = plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.coastlines()
        ax.stock_img()
        
        for city in cities:
            coords = self.get_coordinates(city)
            if coords:
                lat, lon = coords
                # Точка с выбранным цветом
                ax.plot(lon, lat, marker='o', color=marker_color, markersize=5, transform=ccrs.PlateCarree())
                ax.text(lon + 1, lat + 1, city, transform=ccrs.PlateCarree(), fontsize=8)

        plt.title('Ваши города на карте')
        plt.savefig(path)
        plt.close()
        return path


        
    def draw_distance(self, path, city1, city2, marker_color='red', line_color='blue'):
        coords1 = self.get_coordinates(city1)
        coords2 = self.get_coordinates(city2)

        if not coords1 or not coords2:
            return None

        lat1, lon1 = coords1
        lat2, lon2 = coords2

        # Создаем карту
        fig = plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        ax.stock_img()

        # Точки городов
        ax.plot([lon1, lon2], [lat1, lat2], marker='o', color=marker_color, markersize=5, transform=ccrs.PlateCarree())

        # Подписи
        ax.text(lon1 + 1, lat1 + 1, city1, transform=ccrs.PlateCarree(), fontsize=8)
        ax.text(lon2 + 1, lat2 + 1, city2, transform=ccrs.PlateCarree(), fontsize=8)

        # Линия между городами
        ax.plot([lon1, lon2], [lat1, lat2], color=line_color, linewidth=2, transform=ccrs.PlateCarree())

        plt.title(f'Расстояние между {city1} и {city2} 🌍')
        plt.savefig(path)
        plt.close()
        return path



if __name__=="__main__":
    
    m = DB_Map(DATABASE)
    m.create_user_table()

