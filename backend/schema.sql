-- ContentBoost AI Database Schema
-- MySQL Database Setup Script

-- Create database
CREATE DATABASE IF NOT EXISTS contentboost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE contentboost;

-- Drop existing tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS rate_limits;
DROP TABLE IF EXISTS oauth_accounts;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    hashed_password VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- OAuth accounts table
CREATE TABLE oauth_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    provider VARCHAR(50) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token VARCHAR(500),
    refresh_token VARCHAR(500),
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_provider_user (provider, provider_user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_provider (provider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Rate limits table
CREATE TABLE rate_limits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    ip_address VARCHAR(45) NOT NULL,
    request_count INT DEFAULT 0,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_ip_date_user (ip_address, date, user_id),
    INDEX idx_date (date),
    INDEX idx_ip_address (ip_address)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert admin user (password: admin123)
-- Note: Change this password in production!
INSERT INTO users (email, name, hashed_password, role, is_active, is_verified)
VALUES (
    'admin@contentboost.ai',
    'Admin User',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aq7k0GLlOq6e',
    'admin',
    TRUE,
    TRUE
);

-- Verify tables created
SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as user_count FROM users;
SELECT COUNT(*) as oauth_count FROM oauth_accounts;
SELECT COUNT(*) as rate_limit_count FROM rate_limits;
