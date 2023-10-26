-- Create database BookDB;
USE BookDB;

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
