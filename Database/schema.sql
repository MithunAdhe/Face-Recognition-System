CREATE DATABASE IF NOT EXISTS face_recognition;

USE face_recognition;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,   
    name VARCHAR(255) NOT NULL,         
    course VARCHAR(255) NOT NULL,       
    class VARCHAR(255) NOT NULL,        
    face_encoding BLOB NOT NULL          
);
