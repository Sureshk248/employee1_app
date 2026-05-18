from flask import Flask, Response, request, redirect, jsonify, render_template
import sqlite3
import os
import mimetypes
from werkzeug.utils import secure_filename
from flask import send_from_directory
import socket
from ftplib import FTP
from io import BytesIO

from crud.create import create_employee
from crud.update import update_employee
from crud.delete import delete_employee
from crud.read import read_employee
import traceback

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

host = "172.17.4.178"
port = 24

user = "user"
password = "password"


@app.route("/")
def home():
    conn = sqlite3.connect("employee.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    conn.close()

    return render_template("form.html", employees=employees)


@app.route("/uploads/<pernr>")
def uploaded_file(pernr):

    memory_file = BytesIO()

    file = None

    try:

        ftp = FTP()

        ftp.connect(host, port, timeout=10)

        ftp.login(user=user, passwd=password)

        files = ftp.nlst()

        for file1 in files:

            if file1.startswith(pernr.zfill(8)):

                file = file1
                break

        if file:

            ftp.retrbinary("RETR " + file, memory_file.write)

            memory_file.seek(0)

            import mimetypes

            mime_type = mimetypes.guess_type(file)[0]

            return Response(memory_file.getvalue(), mimetype=mime_type)

    except Exception as e:
        pass

    finally:

        try:
            ftp.quit()
        except:
            pass

    # LOCAL FALLBACK
    try:

        for file1 in os.listdir("uploads"):

            if file1.startswith(pernr):

                return send_from_directory("uploads", file1)

    except Exception as e:
        pass

    return "File not found"


@app.route("/submit", methods=["POST"])
def submit():
    pernr = request.form.get("pernr")
    name = request.form.get("name")
    desig = request.form.get("desig")
    dob = request.form.get("dob")
    file = request.files["attachment"]

    filename = ""

    if file.filename != "":

        filename = secure_filename(file.filename)

        filename = pernr + "_" + filename

        upload_path = os.path.join("uploads", filename)

        file.save(upload_path)

        print("File uploaded:", filename)

    action = request.form.get("action")
    read_employee(pernr)
    print(action)
    if read_employee(pernr)["status"] == "S":
        print(action)
        if action == "delete":
            delete_employee(pernr)
        else:
            update_employee(pernr, name, desig, dob, filename)
    else:
        create_employee(pernr, name, desig, dob, filename)

    return redirect("/")


if __name__ == "__main__":
    app.run()
