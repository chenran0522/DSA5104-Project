import mysql.connector
import json

# 数据库连接配置
config = {
    'user': 'root',
    'password': '...',
    'host': '127.0.0.1',
    'database': 'BookDB',
    'raise_on_warnings': True
}

# 与MySQL建立连接
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# 用于存储已插入的genres和cast，避免重复插入
inserted_name = set()
inserted_casts = set()
with open("../../data/json/book.json", 'r', encoding='utf-8') as file:
#with open("../../data/json/book.json", 'r') as file:
    data = json.load(file)  # 读取整个JSON文件为一个列表
    #for line in file:
     #   item = json.loads(line)

    for item in data:
        # 插入Image数据
        cursor.execute("INSERT IGNORE INTO Book (book_id, title, rating, watch_numbers,score, type_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (item['id'], item['title'], item['rating'],item['watch_numbers'],  item['score'], item['type_id']))

        # 处理并插入genres数据l
        #genres = item.get('genres', [])
        authors_name=item.get('author',[])
        for author_name in authors_name:
            if author_name not in inserted_name:
                cursor.execute(
                    "INSERT INTO Authors (author_name) VALUE(%s)", (author_name,))
                inserted_name.add(author_name)
            cursor.execute(
                "SELECT author_id FROM Authors WHERE author_name = %s;", (author_name,))
            author_id = cursor.fetchone()[0]
            book_id = item['id']
            cursor.execute(
                "INSERT INTO Book_author (book_id, author_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE book_id=book_id, author_id=author_id",
                (book_id, author_id))

        # 提交事务
        conn.commit()

# 关闭连接
cursor.close()
conn.close()
