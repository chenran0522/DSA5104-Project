from flask import Blueprint, jsonify, json, request, make_response
from bson import ObjectId
import mysql.connector
from pymongo import MongoClient

bp = Blueprint('book_queries', __name__)


def json_encoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(
        f"Object of type {type(o).__name__} is not JSON serializable")


@bp.route('/search_book', methods=['POST']) #模糊查询
def search_book():
    title = request.json['title']

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book WHERE title LIKE CONCAT('%', '{title}', '%') ")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
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



@bp.route('/search_book_by_id', methods=['POST']) 
def search_book_by_id():
    book_id = int(request.json['id'])

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book WHERE book_id = '{book_id}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.find({"id": book_id}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response




@bp.route('/search_book_by_author_name', methods=['POST']) #作者名字查
def search_book_by_author_name():
    author_name = request.json['author_name']
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book join book_author on book.book_id = book_author.book_id join authors on authors.author_id = book_author.author_id WHERE authors.author_name like CONCAT('%', '{author_name}', '%')")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    regex_pattern = f".*{author_name}.*"
    query = {"author": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response



@bp.route('/search_book_by_rating', methods=['POST']) #评分高于多少
def search_book_by_rating():
    rating = float(request.json['rating'])

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book WHERE book.rating >= '{rating}'")
    mysql_result = cursor.fetchall ()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.find({"rating": {"$gte": rating}}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response


@bp.route('/search_book_by_watch_numbers', methods=['POST']) #watch_numbers高于多少
def search_book_by_watch_numbers():
    watch_numbers = int(request.json['watch_numbers'])

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book WHERE book.watch_numbers >= '{watch_numbers}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.find({"watch_numbers": {"$gte": watch_numbers}}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response


@bp.route('/find_top_rated_book', methods=['POST'])#查询top n rating book
def find_top_rated_book():
    top = int(request.json['top'])
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book ORDER BY rating DESC LIMIT {top}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.find().sort([("rating", -1)]).limit(top))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response



@bp.route('/find_top_score_book', methods=['POST'])#查询top n score book
def find_top_score_book(limit=10):
    top = request.json['top']
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book ORDER BY score DESC LIMIT {top}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.find().sort([("score", -1)]).limit(top))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_top_watch_numbers_book', methods=['POST'])#查询top n watch_numbers book
def find_top_watch_numbers_book(limit=10):
    top = int(request.json['top'])
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book ORDER BY watch_numbers DESC LIMIT {top}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.find().sort([("watch_numbers", -1)]).limit(top))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response


@bp.route('/find_random_book', methods=['POST']) #随机查询
def find_random_book():
    num = int(request.json['num'])
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM book ORDER BY RAND() LIMIT {num}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']
    mongo_results = list(mongo_collection.aggregate([{"$sample": {"size": num}}]))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_book_all', methods=['POST']) #全面模糊查询
def find_book_all():
    author_name = request.json.get('author_name', '')
    title = request.json.get('title', '')
    rating = float(request.json.get('rating', 0))
    watch_numbers = int(request.json.get('watch_numbers', 0))
    score = int(request.json.get('score', 0))

    # 连接MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="bookdb"
    )
    cursor = mydb.cursor()

    cursor.execute(f"use systemdatabase")
    # 构建MySQL查询
    mysql_query = f"""SELECT * FROM book
                      WHERE book_id IN
                        (SELECT ba.book_id 
                        FROM book_author AS ba
                        JOIN authors AS a ON ba.author_id = a.author_id
                        WHERE a.author_name LIKE CONCAT('%', '{author_name}', '%'))
                      AND title LIKE CONCAT('%', '{title}', '%')
                      AND score >= {score}
                      AND rating >= {rating}
                      AND watch_numbers >= {watch_numbers}
                      ORDER BY rating DESC
                      LIMIT 10"""

    cursor.execute(mysql_query)
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['book']

    # 构建MongoDB聚合管道
    pipeline = [
        {
            "$match": {
                "author": {"$regex": author_name, "$options": "i"},
                "title": {"$regex": title, "$options": "i"},
                "score": {"$gte": score},
                "rating": {"$gte": rating},
                "watch_numbers": {"$gte": watch_numbers},
            }
        },
        {
            "$sort": {"rating": -1}
        },
        {
            "$limit": 10
        }
    ]

    mongo_results = list(mongo_collection.aggregate(pipeline))

    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response