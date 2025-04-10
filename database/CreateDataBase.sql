CREATE DATABASE IF NOT EXISTS auth;

use auth;

CREATE TABLE IF NOT EXISTS USERS (
    id char(36) primary key default (uuid()),
    username varchar(30) not null unique,
    password varchar(255) not null,
    role varchar(30),
);

SELECT * FROM users;