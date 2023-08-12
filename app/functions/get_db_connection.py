import MySQLdb

def get_db_connection():
    db_host = os.environ.get("DB_HOST", "localhost")
    db_user = os.environ.get("DB_USER", "root")
    db_password = os.environ.get("DB_PASSWORD", "")
    db_name = os.environ.get("DB_NAME", "")

    return MySQLdb.connect(host=db_host, user=db_user, passwd=db_password, db=db_name)
