# Verwenden des Python-Images als Basis
FROM python:3.8

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Installieren von 'jq', 'wget' und unzip
RUN apt-get update && \
    apt-get install -y jq wget unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Kopieren der Abhängigkeiten in den Container
COPY requirements.txt requirements.txt

# Installieren der Python-Abhängigkeiten
RUN pip install -r requirements.txt

# Kopieren des restlichen App-Codes in den Container
COPY app app

# Erstelle tmp-Ordner
RUN mkdir tmp

# Erstelle Bootstrap tmp-dir
RUN mkdir tmp/bootstrap

# Lade Bootstrap herunter
RUN wget -O tmp/bootstrap.zip "$(curl -s https://api.github.com/repos/twbs/bootstrap/releases/latest | jq -r '.assets[0].browser_download_url')" 

# Entpacke das Bootstrap-Archiv im Tempordner
RUN unzip tmp/bootstrap.zip -d tmp/bootstrap && rm tmp/bootstrap.zip

# Verschiebe der Bootstrap Daten
RUN find tmp/bootstrap/ -name 'bootstrap.css' -exec mv {} app/static/css/ \; \
    -o -name 'bootstrap.min.css' -exec mv {} app/static/css/ \; \
    -o -name 'bootstrap.rtl.css' -exec mv {} app/static/css/ \; \
    -o -name 'bootstrap.rtl.min.css' -exec mv {} app/static/css/ \; \
    -o -name 'bootstrap.bundle.js' -exec mv {} app/static/js/ \; \
    -o -name 'bootstrap.bundle.min.js' -exec mv {} app/static/js/ \;

# Löschen des Bootstrapverzeichnes
RUN rm -rf tmp/*

# Herunterladen des popper.min.js
RUN popper_url="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" && \
    popper_filename=$(basename "$popper_url") && \
    wget "$popper_url" && \
    mv "$popper_filename" app/static/js/

# Herunterladen von jquery-3.2.1.slim.min.js
RUN jquery_url="https://code.jquery.com/jquery-3.2.1.slim.min.js" && \
    jquery_filename=$(basename "$jquery_url") && \
    wget "$jquery_url" && \
    mv "$jquery_filename" app/static/js/

# Löschen des temporären Verzeichnisses
RUN rm -rf tmp 

# Exponieren des gewünschten Ports
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["python", "-m", "app.app"]
