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
-- Create database BookDB;



-- 删除已存在的表，如果需要的话
DROP TABLE IF EXISTS Book_author;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Book;

-- 重新创建表
CREATE TABLE Book (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
	rating INT,
	watch_numbers INT,
   	score INT, 
    type_id INT
);

CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    Author_name VARCHAR(255) UNIQUE
);

CREATE TABLE Book_author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);


-- create DATABASE MusicDB;
USE MusicDB;

-- 删除已存在的表，如果需要的话
DROP TABLE IF EXISTS Music_Artist;
DROP TABLE IF EXISTS Music_genres;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Music;
DROP TABLE IF EXISTS genres;

-- 重新创建表
CREATE TABLE Music (
    music_id INT PRIMARY KEY,
    music_name VARCHAR(255),
    rating FLOAT,
    play_count INT,
    type_id INT
);


CREATE TABLE Music_genres (
    music_id INT,
    genre_id INT,
    PRIMARY KEY (music_id, genre_id),
    FOREIGN KEY (music_id) REFERENCES Music(music_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE Artist (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_name VARCHAR(255) unique
);

CREATE TABLE Music_Artist (
    music_id INT,
    artist_id INT,
    PRIMARY KEY (music_id, artist_id),
    FOREIGN KEY (music_id) REFERENCES Music(music_id),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);
USE userdb;

-- 删除已存在的表，如果需要的话
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Evaluation;

-- 重新创建表
CREATE TABLE User (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255));


CREATE TABLE Evaluation (
    user_id INT,
    type_id INT,
    target_id INT,
    PRIMARY KEY (user_id, type_id, target_id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);
