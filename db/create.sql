CREATE DATABASE posts_db;

CREATE USER 'wobot_user'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'wobot';

GRANT ALL PRIVILEGES ON posts_db.* TO 'wobot_user'@'localhost';
