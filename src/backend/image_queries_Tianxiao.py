from flask import Blueprint, jsonify, json, request, make_response
from bson import ObjectId
import mysql.connector
from pymongo import MongoClient

bp = Blueprint('image_queries', __name__)


def json_encoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(
        f"Object of type {type(o).__name__} is not JSON serializable")


@bp.route('/search_image', methods=['POST'])
def search_image():
    title = request.json['title']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE name = '{title}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"title": title}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/search_image_fuzzy', methods=['POST'])
def search_image_fuzzy():
    title = request.json['title']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE name  LIKE CONCAT('%', '{title}', '%') ")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    regex_pattern = f".*{title}.*"
    query = {"title": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response


@bp.route('/search_image_by_id', methods=['POST'])
def search_image_by_id():
    image_id = request.json['image_id']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE image_id = '{image_id}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"id": image_id}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response


@bp.route('/search_image_by_format', methods=['POST'])
def find_images_by_type():
    format = request.json['format']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image WHERE format = '{format}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"format": format}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_top_rated_images', methods=['POST'])
def find_top_rated_images(limit=10):

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image ORDER BY rating DESC LIMIT 10")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find().sort([("rating")]).limit(10))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_random_images', methods=['POST'])
def find_random_images(limit=10):
    num = request.json['num']
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM image ORDER BY RAND() LIMIT {num}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.aggregate([{"$sample": {"size": num}}]))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response