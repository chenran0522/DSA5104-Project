import mysql.connector
import json

# 数据库连接配置
config = {
    'user': 'root',
    'password': 'cr003265...',
    'host': '127.0.0.1',
    'database': 'EvaluationDB',
    'raise_on_warnings': True
}   

# 与MySQL建立连接
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

with open("../../data/json/evaluation.json", 'r') as file:
    for line in file:
        data = json.loads(line.strip())

        # 插入Image数据
        cursor.execute("INSERT IGNORE INTO Image (type_id, target_id, user_id, score, comment) VALUES (%s, %s, %s, %s, %s)",
                       (data['type_id'], data['target_id'], data['user_id'], data['score'], data['comment']))

        # 提交事务
        conn.commit()

# 关闭连接
cursor.close()
conn.close()
