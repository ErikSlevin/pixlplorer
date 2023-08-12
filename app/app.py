import os, sys, MySQLdb, logging, inspect
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps

from app.functions.get_db_connection import get_db_connection
from app.functions.setup_database import setup_database

app = Flask(__name__)

# Konfiguration des Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

setup_database()

# Weise den Routen URLs zu
from app.routes.index_route import index
app.route('/')(index)

from app.routes.upload_route import upload
app.route('/upload', methods=['POST'])(upload)

if __name__ == "__main__":
    logger.info("Datenbank-Setup abgeschlossen.")
    app.run(host='0.0.0.0', port=5000)
