import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import MySQLdb
from app.functions.get_db_connection import get_db_connection


def upload_image():
    # Erstelle den "uploads"-Ordner, wenn er nicht existiert
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    if image_file:
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join("uploads", filename))  # Save image to "uploads" directory

        # Get image dimensions using PIL
        image_path = os.path.join("uploads", filename)
        with Image.open(image_path) as img:
            image_height, image_width = img.size

        # Extract extension from the uploaded image
        image_extension = filename.split('.')[-1]

        # Construct image URLs
        base_url = request.host_url.rstrip('/')  # Get base URL of the current request
        image_url = f"{base_url}/uploads/{filename}"
        thumbnail_name = f"{filename.split('.')[0]}_thumbnail.{image_extension}"
        thumbnail_url = f"{base_url}/uploads/{thumbnail_name}"

        image_file_size = os.path.getsize(image_path)

        # Extract tags and categories from the form
        tags = request.form.get('tags', '').split(',')
        categories = request.form.get('categories', '').split(',')

        # Insert extension into the extensions table
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        cursor.execute("SELECT id FROM extensions WHERE extension = %s", (image_extension,))
        existing_extension = cursor.fetchone()
        if existing_extension:
            extension_id = existing_extension[0]
        else:
            cursor.execute("INSERT INTO extensions (extension) VALUES (%s)", (image_extension,))
            extension_id = cursor.lastrowid

        # Insert dimensions into the dimensions table
        cursor.execute("SELECT id FROM dimensions WHERE height = %s AND width = %s", (image_height, image_width))
        existing_dimensions = cursor.fetchone()
        if existing_dimensions:
            dimension_id = existing_dimensions[0]
        else:
            cursor.execute("INSERT INTO dimensions (height, width) VALUES (%s, %s)", (image_height, image_width))
            dimension_id = cursor.lastrowid

        # Insert information into the database
        cursor.execute("INSERT INTO images (url) VALUES (%s)", (image_url,))
        image_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO image_details (image_id, extension_id, dimension_id, file_size, thumbnail_name, thumbnail_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (image_id, extension_id, dimension_id, image_file_size, thumbnail_name, thumbnail_url))

        for tag in tags:
            cursor.execute("SELECT tag_name FROM tags WHERE tag_name = %s", (tag,))
            existing_tag = cursor.fetchone()
            if existing_tag:
                tag_name = existing_tag[0]
            else:
                cursor.execute("INSERT INTO tags (tag_name) VALUES (%s)", (tag,))
                tag_name = tag
            cursor.execute("INSERT INTO image_tags (image_id, tag_id) SELECT %s, id FROM tags WHERE tag_name = %s", (image_id, tag_name))

        for category in categories:
            cursor.execute("SELECT category_name FROM categories WHERE category_name = %s", (category,))
            existing_category = cursor.fetchone()
            if existing_category:
                category_name = existing_category[0]
            else:
                cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (category,))
                category_name = category
            cursor.execute("INSERT INTO image_categories (image_id, category_id) SELECT %s, id FROM categories WHERE category_name = %s", (image_id, category_name))

        cursor.close()
        db_conn.commit()
        db_conn.close()

        return jsonify({"message": "Image uploaded successfully"}), 200

    return jsonify({"error": "Upload failed"}), 500
