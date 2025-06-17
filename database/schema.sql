CREATE DATABASE reservas_db;
USE reservas_db;

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NOT NULL,
    service VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);