-- Vérifier si la base de données existe, sinon la créer
CREATE DATABASE IF NOT EXISTS app_database;
USE app_database;

-- Création de la table des utilisateurs avec des améliorations
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Identifiant unique de l'utilisateur
    username VARCHAR(50) UNIQUE NOT NULL, -- Nom d'utilisateur (unique)
    email VARCHAR(100) UNIQUE NOT NULL COLLATE utf8_general_ci, -- Adresse email (unique et insensible à la casse)
    password_hash VARCHAR(255) NOT NULL, -- Mot de passe hashé pour plus de sécurité
    user_type ENUM('student', 'instructor', 'client','freelancer') DEFAULT 'student', -- Type de l'utilisateur (étudiant par défaut)
    is_active TINYINT(1) DEFAULT 1, -- Indique si le compte est actif (1 = actif, 0 = désactivé)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date et heure de création du compte
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Date et heure de la dernière mise à jour
);

-- Création d'index pour améliorer les performances des requêtes de recherche
CREATE INDEX idx_email ON users(email); -- Index sur l'email pour accélérer les recherches
CREATE INDEX idx_username ON users(username); -- Index sur le nom d'utilisateur