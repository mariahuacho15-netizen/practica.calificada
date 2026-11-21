import os
import sqlite3
from datetime import date
from functools import wraps

from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-secreta-de-desarrollo")
DATABASE = os.path.join(os.path.dirname(__file__), "gastos.db")

USUARIO = "admin"
CLAVE = "123"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as con:
        con.execute(
            """CREATE TABLE IF NOT EXISTS gastos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   fecha TEXT NOT NULL,
                   descripcion TEXT NOT NULL,
                   monto REAL NOT NULL)"""
        )


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("usuario"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (request.form.get("usuario") == USUARIO
                and request.form.get("clave") == CLAVE):
            session["usuario"] = USUARIO
            return redirect(url_for("index"))
        flash("Usuario o clave incorrectos", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    db = get_db()
    if request.method == "POST":
        fecha = request.form.get("fecha", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        try:
            monto = float(request.form.get("monto", ""))
        except ValueError:
            monto = None
        if not fecha or not descripcion or monto is None or monto <= 0:
            flash("Completa todos los campos con un monto válido", "error")
        else:
            db.execute(
                "INSERT INTO gastos (fecha, descripcion, monto) VALUES (?,?,?)",
                (fecha, descripcion, monto))
            db.commit()
            flash("Gasto registrado", "ok")
        return redirect(url_for("index"))
    gastos = db.execute(
        "SELECT * FROM gastos ORDER BY fecha DESC, id DESC").fetchall()
    return render_template("index.html", gastos=gastos,
                           hoy=date.today().isoformat())


@app.route("/eliminar/<int:gasto_id>", methods=["POST"])
@login_required
def eliminar(gasto_id):
    db = get_db()
    db.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
    db.commit()
    flash("Gasto eliminado", "ok")
    return redirect(url_for("index"))


@app.route("/reporte")
@login_required
def reporte():
    desde = request.args.get("desde", "")
    hasta = request.args.get("hasta", "")
    sql, params = "SELECT * FROM gastos WHERE 1=1", []
    if desde:
        sql += " AND fecha >= ?"
        params.append(desde)
    if hasta:
        sql += " AND fecha <= ?"
        params.append(hasta)
    sql += " ORDER BY fecha, id"
    db = get_db()
    gastos = db.execute(sql, params).fetchall()
    total = sum(g_["monto"] for g_ in gastos)
    por_mes = {}
    for g_ in gastos:
        por_mes[g_["fecha"][:7]] = por_mes.get(g_["fecha"][:7], 0) + g_["monto"]
    promedio = total / len(gastos) if gastos else 0
    return render_template("reporte.html", gastos=gastos, total=total,
                           por_mes=por_mes, promedio=promedio,
                           desde=desde, hasta=hasta)


init_db()

if __name__ == "__main__":
    app.run(debug=True)
