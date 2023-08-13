import os, sys, MySQLdb, logging, inspect
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps

from app.functions.get_db_connection import get_db_connection
from app.functions.setup_database import setup_database

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Konfiguration des Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Weise den Routen URLs zu
from app.routes.index_route import index
app.route('/')(index)

from app.routes.upload_route import upload
app.route('/upload', methods=['POST'])(upload)

from app.routes.setup_routes import setup_step1
app.route('/setup', methods=['GET', 'POST'])(setup_step1)

from app.routes.setup_routes import setup_step2
app.route('/setup/step2', methods=['GET', 'POST'])(setup_step2)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
