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

# Exponieren des gewünschten Ports
EXPOSE 5000

# Starten der Flask-Anwendung
CMD ["python", "-m", "app.app"]
