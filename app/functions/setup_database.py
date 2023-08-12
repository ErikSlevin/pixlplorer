# app/functions/setup_database.py
import os
import MySQLdb

def setup_database():
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "")


    # Verbindung zur Datenbank herstellen
    db_connection = MySQLdb.connect(
        host=db_host,
        user=db_user,
        passwd=db_password
    )

    # Cursor erstellen
    cursor = db_connection.cursor()

    # Datenbank erstellen
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    # Zur pixlplorer-Datenbank wechseln
    cursor.execute(f"USE {db_name}")

    # Tabelle extensions erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extensions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            extension VARCHAR(10) NOT NULL
        )
    """)

    # Tabelle dimensions erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dimensions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            height INT,
            width INT
        )
    """)

    # Tabelle images erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabelle image_details erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_id INT,
            extension_id INT,
            dimension_id INT,
            file_size INT,
            thumbnail_name VARCHAR(255),
            thumbnail_url VARCHAR(255),
            FOREIGN KEY (image_id) REFERENCES images(id),
            FOREIGN KEY (extension_id) REFERENCES extensions(id),
            FOREIGN KEY (dimension_id) REFERENCES dimensions(id)
        )
    """)

    # Tabelle tags erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tag_name VARCHAR(50) NOT NULL
        )
    """)

    # Tabelle image_tags erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_tags (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_id INT,
            tag_id INT,
            FOREIGN KEY (image_id) REFERENCES images(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id)
        )
    """)

    # Tabelle categories erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(50) NOT NULL
        )
    """)

    # Tabelle image_categories erstellen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS image_categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_id INT,
            category_id INT,
            FOREIGN KEY (image_id) REFERENCES images(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    # Verbindung schließen
    cursor.close()
    db_connection.close()
