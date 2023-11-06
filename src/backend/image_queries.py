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
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image WHERE name = '{title}'")
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
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image WHERE name  LIKE CONCAT('%', '{title}', '%') ")
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
    image_id = int(request.json['image_id'])

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image WHERE image_id = '{image_id}'")
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
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image WHERE format = '{format}'")
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


@bp.route('/find_pop_images', methods=['POST'])#查询top热度image
def find_pop_images(limit=10):
    num = int(request.json['Num'])
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image ORDER BY watch_numbers DESC LIMIT {num}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find().sort([("watch_numbers",-1)]).limit(num))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response



@bp.route('/find_top_rated_images', methods=['POST'])#查询top热度image
def find_top_rated_images(limit=10):
    num = int(request.json['Num'])
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image ORDER BY rating DESC LIMIT {num}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find().sort([("rating",-1)]).limit(num))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_random_images', methods=['POST'])#随机查询
def find_random_images(limit=10):
    num = int(request.json['Num'])
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image ORDER BY RAND() LIMIT {num}")
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

@bp.route('/find_images_by_genres', methods=['POST'])#查询image类型
def find_images_by_genres():
    genre = request.json['genre']
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT * FROM image as I natural join image_genre as IG where IG.genre_id = (SELECT genre_id from genres where name = '{genre}')")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    mongo_results = list(mongo_collection.find({"genres": genre}))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_images_by_cast', methods=['POST'])#模糊查询演员
def find_images_by_cast():
    cast = request.json['cast']
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM systemdatabase.image as I natural join image_cast as IC where IC.cast_id in (SELECT cast_id from cast_info where cast_name like concat ('%', '{cast}', '%'));")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    regex_pattern = f".*{cast}.*"
    query = {"cast": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

@bp.route('/find_images', methods=['POST']) # 综合（模糊title、模糊cast、genre、高分要求、format、默认输出rating最高的10个）
def find_images():
    cast = request.json.get('cast', '')
    title = request.json.get('title', '')
    genre = request.json.get('genre', '')
    rating = float(request.json.get('rating', 0))
    format = request.json.get('format', '')
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107",
        database="imagedb"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"SELECT distinct image_id,format,name,rating,watch_numbers,type_id FROM (SELECT * FROM image as I natural join image_cast as IC where IC.cast_id in (SELECT cast_id from cast_info where cast_name like concat ('%', '{cast}', '%'))) as table1 natural JOIN (SELECT * FROM image WHERE name  LIKE CONCAT('%', '{title}', '%') ) as table2 where rating > {rating} and table1.format LIKE CONCAT('%', '{format}', '%')  and table1.image_id in( SELECT I.image_id FROM image as I natural join image_genre as IG where IG.genre_id in (SELECT genre_id from genres where name LIKE CONCAT('%', '{genre}', '%'))) order by rating limit 10;")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    genre_to_find = genre  # 要查询的 genre 值
    name_to_find = cast  # 模糊匹配的 name 模式
    title_to_find = title  # 模糊匹配的 title 模式
    rate_threshold = rating  # 最低 rating 阈值
    format_to_find = format  # 要查询的 format 值

    # 创建聚合管道
    pipeline = [
        {
            "$match": {
                "genres": {"$regex": genre_to_find, "$options": "i"},
                "cast": {"$regex": name_to_find, "$options": "i"},
                "title": {"$regex": title_to_find, "$options": "i"},
                "rating": {"$gte": rate_threshold},
                "format": {"$regex": format_to_find, "$options": "i"},
            }
        },
        {
            "$sort": {"rating": -1}  # 按 rating 从高到低排序
        },
        {
            "$limit": 10  # 返回最多十个结果
        }
    ]

    # 执行聚合查询
    mongo_results = list(mongo_collection.aggregate(pipeline))
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response


@bp.route('/find_images_join', methods=['POST']) # 综合（模糊title或模糊cast）
def find_images_join():
    cast = request.json.get('title', '')
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="ytx918107"
    )
    cursor = mydb.cursor()
    cursor.execute(f"use systemdatabase")
    cursor.execute(f"(select distinct * from image where image_id in (select image_id from image natural join image_cast natural join cast_info where cast_name like concat ('%', '{cast}', '%'))) union(select distinct * from image where image_id in (select distinct image_id from image natural join image_cast natural join cast_info where name like concat ('%', '{cast}', '%')));")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['DSA5104']
    mongo_collection = mongo_db['image']
    name_to_find = cast  # 模糊匹配的 name 模式

    # 创建聚合管道
    pipeline = [
        {
            "$match": {
                "cast": {"$regex": name_to_find, "$options": "i"},
            }
        },
        {
            "$sort": {"rating": -1}  # 按 rating 从高到低排序
        }
    ]

    # 执行聚合查询
    mongo_results = list(mongo_collection.aggregate(pipeline))
    pipeline2 = [
        {
            "$match": {
                "title": {"$regex": name_to_find, "$options": "i"},
            }
        },
        {
            "$sort": {"rating": -1}  # 按 rating 从高到低排序
        }
    ]
                
    data = {
        "mysql_data": mysql_result,
        "mongo_data": mongo_results
    }

    mongo_results += list(mongo_collection.aggregate(pipeline2))
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = 'application/json'
    return response

