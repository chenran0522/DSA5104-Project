import mysql.connector
import json

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'Wxp-0525',
    'host': '127.0.0.1',
    'database': 'gameDB',
    'raise_on_warnings': True
}

# 与MySQL建立连接
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 用于存储已插入的genres和cast，避免重复插入
inserted_genres = set()
inserted_directors = set()
with open("../../data/json/game.json", 'r') as file:
    for line in file:
        data = json.loads(line.strip())

        # 插入Image数据
        cursor.execute("INSERT IGNORE INTO game (game_id, name, year, plot, rating, type_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (data['id'], data['name'], data['year'], data['plot'], data['rating'], data['type_id']))

        # 处理并插入genres数据
        genres = data.get('genres')
        if genres:
            for genre in genres:
                if genre not in inserted_genres:
                    cursor.execute(
                        "INSERT INTO genres (name) VALUES (%s)", (genre,))
                    inserted_genres.add(genre)
                cursor.execute(
                    "SELECT genre_id FROM genres WHERE name = %s;", (genre,))
                genre_id = cursor.fetchone()[0]
                game_id = data['id']
                cursor.execute(
                    "INSERT INTO game_genre (game_id, genre_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE game_id=game_id, genre_id=genre_id",
                    (game_id, genre_id))

        # 处理并插入director数据
        director_list = data.get('director')
        if director_list:
            for director in director_list:
                if director not in inserted_directors:
                    cursor.execute(
                        "INSERT INTO director_info (director_name) VALUES (%s) ON DUPLICATE KEY UPDATE director_name=director_name",
                        (director,))
                    inserted_directors.add(director)
                cursor.execute(
                    "SELECT director_id FROM director_info WHERE director_name = %s;", (director,))
                director_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO image_director (game_id, director_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE game_id=game_id",
                    (data['id'], director_id))

        # 提交事务
        conn.commit()

# 关闭连接
cursor.close()
conn.close()