USE ImageDB;

-- 删除已存在的表，如果需要的话
DROP TABLE IF EXISTS image_cast;
DROP TABLE IF EXISTS Image_genre;
DROP TABLE IF EXISTS Cast_info;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS Image;

-- 重新创建表
CREATE TABLE Image (
    image_id INT PRIMARY KEY,
    format VARCHAR(255),
    name VARCHAR(255),
    rating FLOAT,
    watch_numbers INT,
    RUN_Time INT,
    type_id INT
);

CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE Image_genre (
    image_id INT,
    genre_id INT,
    PRIMARY KEY (image_id, genre_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE Cast_info (
    cast_id INT AUTO_INCREMENT PRIMARY KEY,
    cast_name VARCHAR(255) UNIQUE
);

CREATE TABLE image_cast (
    image_id INT,
    cast_id INT,
    PRIMARY KEY (image_id, cast_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id),
    FOREIGN KEY (cast_id) REFERENCES Cast_info(cast_id)
);
