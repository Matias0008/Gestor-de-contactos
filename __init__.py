# Carpeta inicial.
import os
from re import A
from flask import Flask, render_template, request, url_for, redirect, flash
from .db import *

init_db()

def createApp():
    app = Flask(__name__)
    init_db()
    app.config.from_mapping(
        SECRET_KEY="mikey",
        DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        DATABASE=os.environ.get("FLASK_DATABASE"),
    )

    @app.route("/")
    def index():
        db, c = get_db()
        c.execute("SELECT * FROM contacts")
        data = c.fetchall()

        newData = request.args.get('buscar')

        if newData:
            c.execute(
                'SELECT * FROM contacts WHERE nombre LIKE %s',
                 ('%' + newData + '%', )
            )

            data = c.fetchall()



        c.close()
        return render_template("index.html", contacts = data)

    @app.route("/edit_contact/<string:id>", methods = ["POST", "GET"])
    def get_contact(id):
        db, c = get_db()
        c.execute("SELECT * FROM contacts WHERE id = %s", (id, ))
        data = c.fetchall()
        db.commit()
        return render_template("edit-contact.html", contact= data[0])

    @app.route("/update_contact/<id>", methods = ["POST"])
    def update_contact(id):
        if request.method=="POST":
            nombre = request.form["nombre"]
            telefono = request.form["telefono"]
            correo = request.form["email"]
            db, c = get_db()
            c.execute("UPDATE contacts set nombre= %s, telefono = %s, email = %s WHERE id = %s", 
            (nombre, telefono, correo, id))
            db.commit()
            flash("Contacto actualizado correctamente.")
            return redirect(url_for("index"))

    @app.route("/delete_contact/<string:id>", methods = ["POST", "GET"])
    def delete_contact(id):
        db, c = get_db()
        c.execute("DELETE FROM contacts WHERE id = %s", (id,))
        db.commit()
        flash("Contacto removido correctamente.")
        return redirect(url_for("index"))


    @app.route("/add_contact", methods = ["POST"])
    def add_contact():
        if request.method=="POST":
            nombre = request.form["nombre"]
            telefono = request.form["telefono"]
            email = request.form["email"]

            db, c = get_db()
            c.execute("INSERT INTO contacts (nombre, telefono, email) VALUES (%s, %s , %s)", (nombre, telefono, email))
            db.commit()
            flash("Contacto agregado correctamente.")            

        return redirect(url_for("index"))



    return app

app = createApp()
