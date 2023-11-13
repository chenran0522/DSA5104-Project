# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:05:09 2023

@author: liwei
"""

from flask import Blueprint, jsonify, json, request, make_response
from bson import ObjectId
import mysql.connector
from pymongo import MongoClient

bp = Blueprint("game_queries", __name__)


def json_encoder(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


def connect_to_mysql():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        port=3306,
        password="Wxp-0525",  # 应该从安全的地方获取
        database="systemdatabase",
    )


@bp.route("/search_game", methods=["POST"])  # 模糊查询
def search_game():
    name = request.json["name"]

    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM game WHERE name LIKE CONCAT('%', '{name}', '%') ")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]
    regex_pattern = f".*{name}.*"
    query = {"name": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_game_by_id", methods=["POST"])
def search_game_by_id():
    id = int(request.json["id"])

    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM game WHERE game_id = '{id}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]
    mongo_results = list(mongo_collection.find({"game_id": id}))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_game_by_director_name", methods=["POST"])  # 作者名字查
def search_game_by_director_name():
    director_name = request.json["director_name"]

    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT * FROM game join Game_director on game.game_id = Game_director.game_id join Director_id on Director_id.Director_id = Game_director.Director_id WHERE Director_id.name like CONCAT('%', '{director_name}', '%')"
    )
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]
    regex_pattern = f".*{director_name}.*"
    query = {"director": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_game_by_year", methods=["POST"])  # 查年份
def search_game_by_year():
    year = request.json["year"]

    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM game WHERE year = '{year}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]

    # 查询条件需要与数据集中的年份字段格式一致，即包含双引号
    query = {"year": year}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_game_by_rating", methods=["POST"])  # 评分高于多少
def search_game_by_rating():
    rating = request.json["rating"]

    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM game WHERE game.rating >= '{rating}'")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]

    # 查询条件使用 $gte 操作符来匹配评分高于等于指定值的文档
    query = {"rating": {"$gte": rating}}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/search_game_by_genres", methods=["POST"])  # 查genres
def search_game_by_genres():
    genres = request.json["genres"]

    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT * ,genres.name AS genres_name FROM game join game_genre on game.game_id = game_genre.game_id join genres on genres.genre_id = game_genre.genre_id WHERE genres.name like CONCAT('%', '{genres}', '%')"
    )
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]
    regex_pattern = f".*{genres}.*"
    query = {"genres": {"$regex": regex_pattern, "$options": "i"}}
    mongo_results = list(mongo_collection.find(query))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_top_rated_game", methods=["POST"])  # 查询top n rating book
def find_top_rated_book():
    top = int(request.json["top"])
    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM game ORDER BY rating DESC LIMIT {top}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]
    mongo_results = list(mongo_collection.find().sort([("rating", -1)]).limit(top))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_random_game", methods=["POST"])  # 随机查询
def find_random_book():
    num = int(request.json["num"])
    # Fetch data from MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM game ORDER BY RAND() LIMIT {num}")
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]
    mongo_results = list(mongo_collection.aggregate([{"$sample": {"size": num}}]))
    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response


@bp.route("/find_game_all", methods=["POST"])  # 全面模糊查询
def find_game_all():
    Director_name = request.json.get("Director_name", "")
    name = request.json.get("name", "")
    genres_name = request.json.get("genres_name", "")
    rating = (
        float(request.json.get("rating", 0))
        if request.json.get("rating", "") != ""
        else 0
    )
    year = int(request.json.get("year", 0)) if request.json.get("year", "") != "" else 0

    # 连接MySQL
    mydb = connect_to_mysql()
    cursor = mydb.cursor()

    # 构建MySQL查询
    mysql_query = f"""SELECT *
                        FROM game
                        JOIN Game_director AS gd ON game.game_id = gd.game_id
                        JOIN Director_id AS d ON gd.Director_id = d.Director_id
                        JOIN game_genre AS gg ON game.game_id = gg.game_id
                        JOIN genres AS g ON gg.genre_id = g.genre_id
                        WHERE
                            d.name LIKE CONCAT('%', '{Director_name}', '%')
                        AND g.name LIKE CONCAT('%', '{genres_name}', '%')
                        AND game.name LIKE CONCAT('%', '{name}', '%')
                        AND (game.year = {year} OR {year} = 0)
                        AND (game.rating >= {rating} OR {rating} = 0)
                        ORDER BY game.rating DESC
                        LIMIT 1000;"""

    cursor.execute(mysql_query)
    mysql_result = cursor.fetchall()

    # 连接MongoDB
    mongo_client = MongoClient("localhost", 27017)
    mongo_db = mongo_client["DSA5104"]
    mongo_collection = mongo_db["game"]

    # 构建MongoDB查询条件
    query = {}

    if Director_name:
        query["director"] = {"$regex": f".*{Director_name}.*", "$options": "i"}

    if name:
        query["name"] = {"$regex": f".*{name}.*", "$options": "i"}

    if genres_name:
        query["genres"] = {"$regex": f".*{genres_name}.*", "$options": "i"}

    if rating > 0:
        query["rating"] = {"$gte": rating}

    if year:
        query["year"] = year  # 保留年份字段为字符串

    # 执行MongoDB查询
    mongo_results = list(mongo_collection.find(query).sort("rating", -1).limit(10))

    data = {"mysql_data": mysql_result, "mongo_data": mongo_results}
    response = make_response(json.dumps(data, default=json_encoder), 200)
    response.mimetype = "application/json"
    return response
