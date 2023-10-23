import mysql.connector
import json

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'Wxp-0525',
    'host': '127.0.0.1',
    'database': 'ImageDB',
    'raise_on_warnings': True
}

# 与MySQL建立连接
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 用于存储已插入的genres和cast，避免重复插入
inserted_genres = set()
inserted_casts = set()
with open("../../data/json/image.json", 'r') as file:
    for line in file:
        data = json.loads(line.strip())

        # 插入Image数据
        cursor.execute("INSERT IGNORE INTO Image (image_id, format, name, rating, watch_numbers, RUN_Time, type_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (data['id'], data['format'], data['title'], data['rating'], data['watch_numbers'], data['runtime'], data['type_id']))

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
                image_id = data['id']
                cursor.execute(
                    "INSERT INTO image_genre (image_id, genre_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE image_id=image_id, genre_id=genre_id",
                    (image_id, genre_id))

        # 处理并插入cast数据
        cast_list = data.get('cast')
        if cast_list:
            for cast in cast_list:
                if cast not in inserted_casts:
                    cursor.execute(
                        "INSERT INTO cast_info (cast_name) VALUES (%s) ON DUPLICATE KEY UPDATE cast_name=cast_name",
                        (cast,))
                    inserted_casts.add(cast)
                cursor.execute(
                    "SELECT cast_id FROM Cast_info WHERE cast_name = %s;", (cast,))
                cast_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO image_cast (image_id, cast_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE image_id=image_id",
                    (data['id'], cast_id))

        # 提交事务
        conn.commit()

# 关闭连接
cursor.close()
conn.close()
