USE userdb;

-- 删除已存在的表，如果需要的话

DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS User;

-- 重新创建表
CREATE TABLE User (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255));


CREATE TABLE Evaluation (
    user_id INT,
    type_id INT,
    target_id INT,
    score float,
    comment VARCHAR(255),
    PRIMARY KEY (user_id, type_id, target_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);
