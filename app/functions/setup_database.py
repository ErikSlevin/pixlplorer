# app/functions/setup_database.py
import os
import MySQLdb

def setup_database():
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "")

    try:
        success_messages = []
        error_messages = []

        # Verbindung zur Datenbank herstellen
        db_connection = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password
        )

        # Cursor erstellen
        cursor = db_connection.cursor()

        try:
            # Datenbank erstellen
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            success_messages.append(f"Datenbank {db_name} erstellt")
        except Exception as e:
            error_messages.append(f"Datenbank {db_name} nicht erstellt: {str(e)}")

        # Zur pixlplorer-Datenbank wechseln
        cursor.execute(f"USE {db_name}")

        tables = [
            ("extensions", """
                CREATE TABLE IF NOT EXISTS extensions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    extension VARCHAR(10) NOT NULL
                )
            """),
            ("dimensions", """
                CREATE TABLE IF NOT EXISTS dimensions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    height INT,
                    width INT
                )
            """),
            ("images", """
                CREATE TABLE IF NOT EXISTS images (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    url VARCHAR(255) NOT NULL,
                    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """),
            ("image_details", """
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
            """),
            ("tags", """
                CREATE TABLE IF NOT EXISTS tags (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tag_name VARCHAR(50) NOT NULL
                )
            """),
            ("image_tags", """
                CREATE TABLE IF NOT EXISTS image_tags (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    image_id INT,
                    tag_id INT,
                    FOREIGN KEY (image_id) REFERENCES images(id),
                    FOREIGN KEY (tag_id) REFERENCES tags(id)
                )
            """),
            ("categories", """
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category_name VARCHAR(50) NOT NULL
                )
            """),
            ("image_categories", """
                CREATE TABLE IF NOT EXISTS image_categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    image_id INT,
                    category_id INT,
                    FOREIGN KEY (image_id) REFERENCES images(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)
        ]

        for table_name, create_statement in tables:
            try:
                cursor.execute(create_statement)
                success_messages.append(f"Tabelle {table_name} erstellt")
            except Exception as e:
                error_messages.append(f"Fehler beim Erstellen der Tabelle {table_name}: {str(e)}")

        # Verbindung schließen
        cursor.close()
        db_connection.close()

        return True, success_messages # Erfolgreich

    except Exception as e:
        error_messages.append(str(e))
        print(f"Fehler beim Setup der Datenbank: {str(e)}")
        return False, error_messages
