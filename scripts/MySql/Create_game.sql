USE gamedb;

-- 删除已存在的表，如果需要的话
DROP TABLE IF EXISTS game_genre;
DROP TABLE IF EXISTS Game_director;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS Director_id;
DROP TABLE IF EXISTS Game;

-- 重新创建表
CREATE TABLE Game (
    game_id INT PRIMARY KEY,
    name VARCHAR(255),
    year INT,
    plot VARCHAR(511),
    rating FLOAT,
    type_id INT
);
CREATE INDEX idx_game_id ON my_table(game_id);
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE game_genre (
    game_id INT,
    genre_id INT,
    PRIMARY KEY (game_id, genre_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE Director_id (
    Director_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE Game_director (
    game_id INT,
    director_id INT,
    PRIMARY KEY (game_id, director_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (director_id) REFERENCES Director_id(director_id)
);
