from kakebo import app
import sqlite3
from flask import jsonify, render_template, request  #jsonify hace algo parecido al json.dumps
from kakebo.forms import MovimientosForm

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute("SELECT * FROM movimientos;")

    claves = cur.description
    filas = cur.fetchall()
    movimientos = []
    saldo = 0
    for fila in filas: 
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo
        movimientos.append(d)

    conexion.close()

    return render_template('movimientos.html', datos = movimientos) #movimientos es la lista que hemos creado, no la base de datos movimientos

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:
        if formulario.validate(): #comprueba si se cumplen los validadores que pusimos en los metodos metidos en forms.py Si hay errores nos los informa.
            pass
            #Insertar movimiento en la base de datos
            #Redirect a la ruta /
        else:
            return render_template('alta.html', form = formulario) #esto tiene sentido porque el validate nos va a informar tambien los errores