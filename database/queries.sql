-- Ajouter un nouvel utilisateur lors de l'inscription
INSERT INTO users (username, email, password_hash, user_type) 
VALUES ('nom_utilisateur', 'email@example.com', 'MOT_DE_PASSE_HASHÉ', 'student');
-- Le mot de passe doit être hashé avant d'être inséré dans la base de données

-- Rechercher un utilisateur lors de la connexion (par email ou nom d'utilisateur)
SELECT id, username, password_hash, user_type, is_active 
FROM users 
WHERE email = 'email@example.com' OR username = 'nom_utilisateur';
-- On récupère aussi user_type pour personnaliser l'expérience utilisateur

-- Mettre à jour le mot de passe de l'utilisateur
UPDATE users 
SET password_hash = 'NOUVEAU_MOT_DE_PASSE_HASHÉ', updated_at = CURRENT_TIMESTAMP 
WHERE email = 'email@example.com'; 
-- L'ancien mot de passe doit être vérifié avant cette mise à jour

-- Changer le type de l'utilisateur (par exemple, passer un étudiant à instructeur)
UPDATE users 
SET user_type = 'instructor', updated_at = CURRENT_TIMESTAMP 
WHERE email = 'email@example.com';

-- Désactiver un compte utilisateur (au lieu de le supprimer)
UPDATE users 
SET is_active = 0, updated_at = CURRENT_TIMESTAMP 
WHERE email = 'email@example.com'; 

-- Supprimer définitivement un utilisateur
DELETE FROM users 
WHERE email = 'email@example.com'; 
-- Attention : Cette action est irréversible