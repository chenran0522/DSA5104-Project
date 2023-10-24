import mysql.connector
import json

# 数据库连接配置
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'MusicDB',
    'raise_on_warnings': True
}   

# 与MySQL建立连接
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 用于存储已插入的genres和cast，避免重复插入
inserted_genres = set()
inserted_artist_names = set()

with open('C:/Users/liwei/Desktop/dsa5104/project/music/music.json', 'r') as file:
    for line in file:
        data = json.loads(line.strip())

        # 插入Music数据
        cursor.execute("INSERT IGNORE INTO Music (music_id, music_name, rating, play_count, type_id) VALUES (%s, %s, %s, %s, %s)",
                       (data['id'], data['music_name'], data['rating'], data['play_count'], data['type_id']))

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
                music_id = data['id']
                cursor.execute(
                    "INSERT INTO Music_genres (music_id, genre_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE music_id=music_id, genre_id=genre_id",
                    (music_id, genre_id))

        # 处理并插入cast数据
        artist_list = data.get('artist_name')
        if artist_list:
            for artist_name in artist_list:
                if artist_name not in inserted_artist_names :
                    cursor.execute(
                        "INSERT INTO  Artist(artist_name) VALUES (%s) ON DUPLICATE KEY UPDATE artist_name=artist_name",
                        (artist_name,))
                    inserted_artist_names.add(artist_name)
                cursor.execute(
                    "SELECT artist_id FROM Artist WHERE artist_name = %s;", (artist_name,))
                artist_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO Music_Artist (music_id, artist_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE music_id=music_id",
                    (data['id'], artist_id))

        # 提交事务
        conn.commit()

# 关闭连接
cursor.close()
conn.close()
