CREATE DATABASE MediaDB;
USE MediaDB;

CREATE TABLE movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    director VARCHAR(255),
    release_year YEAR,
    genre VARCHAR(50)
);
