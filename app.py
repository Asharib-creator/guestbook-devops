import os, time
from flask import Flask, request, redirect, render_template_string
import mysql.connector

app = Flask(__name__)
cfg = dict(host=os.getenv("DB_HOST", "db"), user=os.getenv("DB_USER", "appuser"),
           password=os.getenv("DB_PASS", "apppass"), database=os.getenv("DB_NAME", "guestbook"))

def conn():
    for _ in range(30):
        try:
            return mysql.connector.connect(**cfg)
        except mysql.connector.Error:
            time.sleep(2)
    raise RuntimeError("DB unavailable")

def init():
    c = conn(); cur = c.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100),
        message TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.commit(); c.close()

PAGE = """<h1>Guestbook</h1>
<form method=post><input name=name placeholder=Name required>
<input name=message placeholder=Message required><button>Post</button></form>
{% for n, m, t in rows %}<p><b>{{n}}</b>: {{m}} <small>({{t}})</small></p>{% endfor %}"""

@app.route("/", methods=["GET", "POST"])
def index():
    c = conn(); cur = c.cursor()
    if request.method == "POST":
        cur.execute("INSERT INTO messages (name, message) VALUES (%s, %s)",
                    (request.form["name"], request.form["message"]))
        c.commit(); c.close()
        return redirect("/")
    cur.execute("SELECT name, message, created FROM messages ORDER BY id DESC")
    rows = cur.fetchall(); c.close()
    return render_template_string(PAGE, rows=rows)

if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=5000)
