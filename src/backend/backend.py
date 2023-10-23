from flask import Flask, jsonify, request
import mysql.connector
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/query', methods=['POST'])
def query_databases():
    query = request.json.get('query')

    # 连接MySQL
    mysql_conn = mysql.connector.connect(
        user='username', password='password', host='127.0.0.1', database='yourdatabase')
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute(query)
    mysql_results = mysql_cursor.fetchall()
    mysql_conn.close()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['yourmongodb']
    mongo_collection = mongo_db['yourcollection']
    mongo_results = list(mongo_collection.find(query))

    # 返回两个数据库的查询结果
    return jsonify({
        'mysql': mysql_results,
        'mongodb': mongo_results
    })


if __name__ == '__main__':
    app.run(debug=True)
