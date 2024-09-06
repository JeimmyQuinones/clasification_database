CREATE DATABASE IF NOT EXISTS secured_storage;
use secured_storage
CREATE TABLE IF NOT EXISTS financial_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    encrypted_account_number VARCHAR(255) NOT NULL,
    encrypted_transaction_details VARCHAR(255) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS users_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    encrypted_name VARCHAR(255) NOT NULL,
    encrypted_email VARCHAR(255) NOT NULL,
    encrypted_phone_number VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE DATABASE IF NOT EXISTS confidential_records;
use confidential_records

CREATE TABLE IF NOT EXISTS users_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    useremail VARCHAR(255) NOT NULL,
    credit_card_number VARBINARY(255),
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
