import mysql.connector
import json
import re

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'ytx918107',
    'host': '127.0.0.1',
    'database': 'userDB',
    'raise_on_warnings': True
}   

# 与MySQL建立连接
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

with open("../../data/json/user_data.json", 'r') as json_file:
    data = json_file.read()

# 使用正则表达式查找大括号中的数据块
pattern = r'\{[^{}]*\}'
matches = re.findall(pattern, data)

for line in matches:
    data = json.loads(line.strip())

    # 插入Image数据
    cursor.execute("INSERT IGNORE INTO User (user_id, password, name) VALUES (%s, %s, %s)",
                   (data['user_id'], data['password'], data['name']))

    # 提交事务
    conn.commit()

# 关闭连接
cursor.close()
conn.close()
