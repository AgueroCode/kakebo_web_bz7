from kakebo import app
import sqlite3
from flask import jsonify  #hace algo parecido al json.dumps

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute("SELECT * FROM movimientos;")

    claves = cur.description
    filas = cur.fetchall()
    movimientos = []
    for fila in filas: 
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
        movimientos.append(d)

    conexion.close()

    return jsonify(movimientos)