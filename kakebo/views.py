from kakebo import app
import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, flash  #jsonify hace algo parecido al json.dumps
from kakebo.forms import MovimientosForm
from datetime import date

def consultaSQL(query, parametros={}):
    #abrimos la conexion
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    
    #ejecutamos la consultad
    cur.execute(query, parametros)
    
    #obtenemos los datos de la consulta
    claves = cur.description
    filas = cur.fetchall()
    
    #procesamos los datos para devolver una lista de diccionarios. un diccionario por fila.
    resultado = []
    for fila in filas: 
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
        resultado.append(d)

    conexion.close()
    return resultado

def modificaTablaSQL(query, parametros = []):
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute(query, parametros)

    conexion.commit() #esto fija el cambio en la base de datos, confirma el cambio
    conexion.close()

@app.route('/')
def index():
    
    movimientos = consultaSQL("SELECT * FROM movimientos ORDER BY fecha;")

    saldo = 0
    for d in movimientos: 
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo

    return render_template('movimientos.html', datos = movimientos) #movimientos es la lista que hemos creado, no la base de datos movimientos

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:
        if formulario.validate(): #comprueba si se cumplen los validadores que pusimos en los metodos metidos en forms.py Si hay errores nos los informa.

            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)"
            try:
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data])
            
            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                return  render_template('alta.html', form=formulario)

            return redirect(url_for("index")) #Redirect a la ruta /. podria hacerse poniendo simplemente "/" usamos url_for para evitar problemas si cambia la direccion de la ruta
        else:
            return render_template('alta.html', form = formulario) #esto tiene sentido porque el validate nos va a informar tambien los errores

@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('borrar.html')
        return render_template('borrar.html', movimiento=filas[0])
    else:
        try:
            modificaTablaSQL("DELETE FROM movimientos WHERE id=?;", [id])
        except sqlite3.Error as e:
            flash("Se ha producido un error en la base de datos, vuelva a intentarlo", 'error')
            return redirect(url_for('index'))

        flash("Borrado realizado con exito", 'aviso')
        return redirect(url_for('index'))

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('modificar.html')
        registro = filas[0]
        registro['fecha'] = date.fromisoformat(registro['fecha'])

        formulario = MovimientosForm(data=registro)

        return render_template('modificar.html', form=formulario)
    else:
        formulario = MovimientosForm()
        if formulario.validate():
            try:
                modificaTablaSQL("UPDATE movimientos SET fecha = ?, concepto = ?, categoria = ?, esGasto = ?, cantidad = ? WHERE id = ?",
                                [formulario.fecha.data,
                                formulario.concepto.data,
                                formulario.categoria.data,
                                formulario.esGasto.data,
                                formulario.cantidad.data,
                                id]
                )
                flash("Modificacion realizada con exito", "aviso")
                return redirect(url_for("index"))
            except sqlite3.Error as e:
                print("Error en update: ", e)
                flash("Se ha producido un error en acceso a base de datos. Contacte con administrador", "error")
                return render_template('modificar.html', form=formulario)    
        else:
            return render_template('modificar.html', form=formulario)     