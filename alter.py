import sqlite3
from flask import Flask, request, redirect, jsonify, render_template

app = Flask(__name__)

conn = sqlite3.connect("employee.db")

cursor = conn.cursor()

cursor.execute("""
  ALTER TABLE employee ADD COLUMN attachment text   
""")

conn.commit()
conn.close()
