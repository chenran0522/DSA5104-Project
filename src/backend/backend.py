from flask import Flask, jsonify, json, request
from bson import ObjectId
import mysql.connector
from pymongo import MongoClient

from flask_cors import CORS


def json_encoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(
        f"Object of type {type(o).__name__} is not JSON serializable")


app = Flask(__name__)
CORS(app)


@app.route('/search_image', methods=['POST'])
def search_image():
    title = request.json['title']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="cr003265...",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE name = '{title}'")
    mysql_result = cursor.fetchone()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"title": title}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    return app.response_class(
        response=json.dumps(data, default=json_encoder),
        mimetype='application/json'
    )

@app.route('/search_image_by_id', methods=['POST'])
def search_image_by_id():
    image_id = request.json['image_id']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="cr003265...",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE image_id = '{image_id}'")
    #cursor.execute(f"SELECT * FROM image WHERE name = '{title}'")
    mysql_result = cursor.fetchone()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"id": image_id}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    return app.response_class(
        response=json.dumps(data, default=json_encoder),
        mimetype='application/json'
    )

@app.route('/search_image_by_id', methods=['POST'])
def search_image_by_id():
    image_id = request.json['image_id']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="cr003265...",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE image_id = '{image_id}'")
    #cursor.execute(f"SELECT * FROM image WHERE name = '{title}'")
    mysql_result = cursor.fetchone()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"id": image_id}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    return app.response_class(
        response=json.dumps(data, default=json_encoder),
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run(debug=True)
