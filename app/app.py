from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps
import os
import sys
import MySQLdb
import logging
import inspect
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Konfiguration des Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Funktionen
sys.path.append(os.path.dirname(__file__))  # Füge das aktuelle Verzeichnis zum Python-Pfad hinzu
from functions import *

# Logge die importierten Funktionen
imported_functions = [name for name, obj in inspect.getmembers(sys.modules['functions']) if inspect.isfunction(obj)]
logger.info("Importierte Funktionen: %s", ", ".join(imported_functions))

get_db_connection()


# Weise den Routen URLs zu
from routes.index_route import index
app.route('/')(index)

from routes.upload_route import upload
app.route('/upload', methods=['POST'])(upload)

if __name__ == "__main__":
    setup_database()
    logger.info("Datenbank-Setup abgeschlossen.")
    app.run(host='0.0.0.0', port=5000)
