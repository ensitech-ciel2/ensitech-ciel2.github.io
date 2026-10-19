-- ============================================================
-- Base fil rouge "supervision" - BTS CIEL 2e annee
-- Mesures de capteurs installes dans les salles d'un lycee
-- Compatible MariaDB 10.x / MySQL 8
-- Utilisation : sudo mariadb < supervision.sql
-- ============================================================
DROP DATABASE IF EXISTS supervision;
CREATE DATABASE supervision CHARACTER SET utf8mb4;
USE supervision;

-- ---------- Structure ----------
CREATE TABLE salle (
    id_salle  INT AUTO_INCREMENT PRIMARY KEY,
    nom       VARCHAR(30) NOT NULL UNIQUE,
    batiment  CHAR(1)     NOT NULL,
    etage     TINYINT     NOT NULL DEFAULT 0
);

CREATE TABLE capteur (
    id_capteur        INT AUTO_INCREMENT PRIMARY KEY,
    reference         VARCHAR(20) NOT NULL UNIQUE,
    grandeur          VARCHAR(20) NOT NULL,
    unite             VARCHAR(5)  NOT NULL,
    date_installation DATE,
    id_salle          INT,
    CONSTRAINT fk_capteur_salle
        FOREIGN KEY (id_salle) REFERENCES salle(id_salle)
);

CREATE TABLE mesure (
    id_mesure  INT AUTO_INCREMENT PRIMARY KEY,
    horodatage DATETIME     NOT NULL,
    valeur     DECIMAL(6,2) NOT NULL,
    id_capteur INT          NOT NULL,
    CONSTRAINT fk_mesure_capteur
        FOREIGN KEY (id_capteur) REFERENCES capteur(id_capteur)
);

-- ---------- Donnees ----------
INSERT INTO salle (nom, batiment, etage) VALUES
    ('B101', 'B', 1),
    ('B102', 'B', 1),
    ('C201', 'C', 2),
    ('Atelier', 'A', 0),
    ('CDI', 'A', 1);

INSERT INTO capteur (reference, grandeur, unite, date_installation, id_salle) VALUES
    ('DHT22-001',   'temperature', '°C',  '2025-09-08', 1),
    ('DHT22-002',   'humidite',    '%',   '2025-09-08', 1),
    ('SCD30-001',   'co2',         'ppm', '2025-11-17', 2),
    ('DS18B20-001', 'temperature', '°C',  '2026-01-12', 3),
    ('DHT22-003',   'temperature', '°C',  '2026-03-02', 4),
    ('SCD30-002',   'co2',         'ppm', NULL,         NULL);

INSERT INTO mesure (horodatage, valeur, id_capteur) VALUES
    ('2026-09-28 08:00:00',   19.5, 1),
    ('2026-09-28 10:00:00',   21.0, 1),
    ('2026-09-28 12:00:00',   22.5, 1),
    ('2026-09-28 14:00:00',   23.0, 1),
    ('2026-09-28 08:00:00',   48.0, 2),
    ('2026-09-28 10:00:00',   45.5, 2),
    ('2026-09-28 12:00:00',   44.0, 2),
    ('2026-09-28 14:00:00',   43.5, 2),
    ('2026-09-28 08:00:00',  420.0, 3),
    ('2026-09-28 10:00:00',  850.0, 3),
    ('2026-09-28 12:00:00', 1250.0, 3),
    ('2026-09-28 14:00:00',  980.0, 3),
    ('2026-09-28 08:00:00',   18.0, 4),
    ('2026-09-28 10:00:00',   20.5, 4),
    ('2026-09-28 12:00:00',   22.0, 4),
    ('2026-09-28 14:00:00',   24.5, 4),
    ('2026-09-28 08:00:00',   16.5, 5),
    ('2026-09-28 10:00:00',   17.0, 5);
