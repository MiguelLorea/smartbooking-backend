-- Script MySQL por si se quiere usar ese motor en vez de SQLite.
-- La app corre con SQLite por defecto (ver settings.py, DB_ENGINE).

CREATE DATABASE IF NOT EXISTS smartbooking CHARACTER SET utf8mb4;
USE smartbooking;

CREATE TABLE IF NOT EXISTS reservas_usuario (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser TINYINT(1) NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_staff TINYINT(1) NOT NULL,
    is_active TINYINT(1) NOT NULL,
    date_joined DATETIME NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    rol VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS reservas_reserva (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    motivo VARCHAR(200) NOT NULL,
    creada DATETIME NOT NULL,
    usuario_id BIGINT NOT NULL,
    CONSTRAINT fk_reserva_usuario FOREIGN KEY (usuario_id) REFERENCES reservas_usuario(id)
);
