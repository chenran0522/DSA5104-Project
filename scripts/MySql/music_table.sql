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
CREATE INDEX idx_music_id ON my_table(music_id);


CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) unique
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
