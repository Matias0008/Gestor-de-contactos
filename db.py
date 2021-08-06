import mysql.connector
from .schema import instructions

def get_db():
        db = mysql.connector.connect(
            host = "localhost",
            user = "Mati Manager",
            password = "155086803",
            database = "contact"
        )
        c = db.cursor(dictionary=True)

        return db, c

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()