from flask import Blueprint, jsonify, json, request, make_response
from bson import ObjectId
import mysql.connector
from pymongo import MongoClient

bp = Blueprint("music_queries", __name__)


def json_encoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


@bp.route("/search_music", methods=["POST"])
def search_image():
    music_name = request.json["music_name"]

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="Wxp-0525",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT * FROM systemdatabase.music WHERE music_name = '{music_name}'"
    )
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    mongo_results = list(mongo_collection.find({"music_name": music_name}))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_music_fuzzy", methods=["POST"])
def search_image_fuzzy():
    music_name = request.json["music_name"]

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="Wxp-0525",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT * FROM music WHERE music_name  LIKE CONCAT('%', '{music_name}', '%') "
    )
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    regex_pattern = f".*{music_name}.*"
    query = {"music_name": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_music_by_id", methods=["POST"])
def search_music_by_id():
    music_id = request.json["music_id"]

    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="cr003265...",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM music WHERE music_id = '{music_id}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    mongo_results = list(mongo_collection.find({"id": music_id}))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_top_rated_music", methods=["POST"])  # 查询top热度image
def find_top_rated_music(limit=10):
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="cr003265...",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM music ORDER BY rating DESC LIMIT 10")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    mongo_results = list(mongo_collection.find().sort([("rating")]).limit(10))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_random_music", methods=["POST"])  # 随机查询
def find_random_images(limit=10):
    num = request.json["num"]
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="cr003265...",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM music ORDER BY RAND() LIMIT {num}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    mongo_results = list(mongo_collection.aggregate([{"$sample": {"size": num}}]))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_music_by_genres", methods=["POST"])  # 查询image类型
def find_images_by_genres():
    genre = request.json["genre"]
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="cr003265...",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT * FROM music as I natural join music_genres as MG where MG.genre_id = (SELECT genre_id from genres where name = '{genre}')"
    )
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    mongo_results = list(mongo_collection.find({"genres": genre}))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_music_by_artist", methods=["POST"])  # 模糊查询artist
def find_images_by_cast():
    artist = request.json["artist"]
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="cr003265...",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    # cursor.execute(f"SELECT * FROM music as I natural join image_cast as IC where IC.cast_id in (SELECT cast_id from cast_info where cast_name like concat ('%', '{cast}', '%'));")
    cursor.execute(
        f"SELECT * FROM music as I natural join music_artist as MA where MA.artist_id in (SELECT artist_id from artist where artist_name like concat ('%', '{artist}', '%'));"
    )
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    regex_pattern = f".*{artist}.*"
    query = {"artist_name": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route(
    "/find_music", methods=["POST"]
)  # 综合（模糊title、模糊cast、genre、高分要求、format、默认输出rating最高的10个）
def find_images():
    artist = request.json.get("artist", "")
    music_name = request.json.get("music_name", "")
    genre = request.json.get("genre", "")
    rating = float(request.json.get("rating", 0))
    print([rating, type(rating)])
    # format = request.json.get('format', '')
    # Fetch data from MySQL
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="cr003265...",
        database="systemdatabase",
    )
    cursor = mydb.cursor()
    # cursor.execute(f"SELECT * FROM (SELECT * FROM image as I natural join image_cast as IC where IC.cast_id in (SELECT cast_id from cast_info where cast_name like concat ('%', '{cast}', '%'))) as table1 natural JOIN (SELECT * FROM image WHERE name  LIKE CONCAT('%', '{title}', '%') ) as table2 where rating > {rating} and table1.format LIKE CONCAT('%', '{format}', '%')  and table1.image_id in( SELECT I.image_id FROM image as I natural join image_genre as IG where IG.genre_id in (SELECT genre_id from genres where name LIKE CONCAT('%', '{genre}', '%'))) order by rating limit 10;")
    cursor.execute(
        f"SELECT * FROM (SELECT * FROM music as I natural join music_artist as MA where MA.artist_id in (SELECT artist_id from artist where artist_name like concat ('%', '{artist}', '%'))) as table1 natural JOIN (SELECT * FROM music WHERE music_name  LIKE CONCAT('%', '{music_name}', '%') ) as table2 where rating > {rating}  and table1.music_id in( SELECT I.music_id FROM music as I natural join music_genres as IG where IG.genre_id in (SELECT genre_id from genres where name LIKE CONCAT('%', '{genre}', '%'))) order by rating limit 10;"
    )
    mysql_result = cursor.fetchall()
    # print(f"SELECT * FROM (SELECT * FROM music as I natural join music_artist as MA where MA.artist_id in (SELECT artist_id from artist where artist_name like concat ('%', '{artist}', '%'))) as table1 natural JOIN (SELECT * FROM music WHERE music_name  LIKE CONCAT('%', '{music_name}', '%') ) as table2 where rating >{rating}  and table1.music_id in( SELECT I.music_id FROM music as I natural join music_genres as IG where IG.genre_id in (SELECT genre_id from genres where name LIKE CONCAT('%', '{genre}', '%'))) order by rating limit 10;")

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["music"]
    genre_to_find = genre  # 要查询的 genre 值
    name_to_find = artist  # 模糊匹配的 name 模式
    title_to_find = music_name  # 模糊匹配的 title 模式
    rate_threshold = rating  # 最低 rating 阈值
    # format_to_find = format  # 要查询的 format 值

    # 创建聚合管道
    pipeline = [
        {
            "$match": {
                "genres": {"$regex": genre_to_find, "$options": "i"},
                "artist_name": {"$regex": name_to_find, "$options": "i"},
                "music_name": {"$regex": title_to_find, "$options": "i"},
                "rating": {"$gte": rate_threshold},
                # "format": {"$regex": format_to_find, "$options": "i"},
            }
        },
        {"$sort": {"rating": -1}},  # 按 rating 从高到低排序
        {"$limit": 10},  # 返回最多十个结果
    ]

    # 执行聚合查询
    mongo_results = list(mongo_collection.aggregate(pipeline))
    print(mongo_results)
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response
