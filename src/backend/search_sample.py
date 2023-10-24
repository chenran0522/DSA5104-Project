# 主键查询
from datetime import datetime


def find_image_by_id(image_id):
    return db.images.find_one({"_id": ObjectId(image_id)})


SELECT * FROM images WHERE image_id = ?
# 模糊查询


def search_image_by_name(name):
    return db.images.find({"name": {"$regex": name, "$options": 'i'}})


SELECT * FROM images WHERE name LIKE CONCAT('%', ?, '%')
# 分类查询


def find_images_by_type(image_type):
    return db.images.find({"type": image_type})


SELECT * FROM images WHERE type = ?
# 时间范围查询


def find_images_by_date_range(start_date, end_date):
    return db.images.find({"date": {"$gte": start_date, "$lte": end_date}})


SELECT * FROM images WHERE date BETWEEN ? AND ?
# 按评分热度查询


def find_top_rated_images(limit=10):
    return db.images.find().sort("rating", -1).limit(limit)


SELECT * FROM images ORDER BY rating DESC LIMIT ?
# 随机查询


def find_random_images(limit=1):
    return db.images.aggregate([{"$sample": {"size": limit}}])


SELECT * FROM images ORDER BY RAND() LIMIT ?
