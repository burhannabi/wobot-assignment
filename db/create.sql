CREATE DATABASE todo_db;

CREATE USER 'wobot_user' IDENTIFIED WITH caching_sha2_password BY 'wobot';

GRANT ALL PRIVILEGES ON todo_db.* TO 'wobot_user';
