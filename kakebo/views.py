from kakebo import app
import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, flash  #jsonify hace algo parecido al json.dumps
from kakebo.forms import MovimientosForm, FiltraMovimientosForm
from datetime import date
from kakebo.dataaccess import *

dbManager = DBmanager()

@app.route('/', methods=['GET', 'POST'])
def index():
    filtraForm = FiltraMovimientosForm()
    query = "SELECT * FROM movimientos WHERE 1 = 1"
    parametros = []

    if request.method == 'POST':
        if filtraForm.validate():
            if filtraForm.fechaDesde.data != None:
                query += " AND fecha >= ?"
                parametros.append(filtraForm.fechaDesde.data)
            if filtraForm.fechaHasta.data != None:
                query += " AND fecha <= ?"
                parametros.append(filtraForm.fechaHasta.data)
            if filtraForm.texto.data != '':
                query += ' AND concepto LIKE ?'
                parametros.append("%{}%".format(filtraForm.texto.data))
        
    query += " ORDER BY fecha"
    print(query)
    movimientos = dbManager.consultaMuchasSQL(query, parametros)

    saldo = 0
    for d in movimientos: 
        if d['esGasto'] == 0:
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo

    return render_template('movimientos.html', datos = movimientos, formulario = filtraForm) #movimientos es la lista que hemos creado, no la base de datos movimientos

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:
        if formulario.validate(): #comprueba si se cumplen los validadores que pusimos en los metodos metidos en forms.py Si hay errores nos los informa.

            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)"
            try:
                dbManager.modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
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
        registro = dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if not registro:
            flash("El registro no existe", "error")
            return render_template('borrar.html', movimiento={})
        return render_template('borrar.html', movimiento=registro)
    else:
        try:
            dbManager.modificaTablaSQL("DELETE FROM movimientos WHERE id = ?;", [id])
        except sqlite3.Error as e:
            flash("Se ha producido un error en la base de datos, vuelva a intentarlo", 'error')
            return redirect(url_for('index'))

        flash("Borrado realizado con exito", 'aviso')
        return redirect(url_for('index'))

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method == 'GET':
        registro = dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if not registro:
            flash("El registro no existe", "error")
            return render_template('modificar.html', form=MovimientosForm())
        registro['fecha'] = date.fromisoformat(registro['fecha'])

        formulario = MovimientosForm(data=registro)

        return render_template('modificar.html', form=formulario)
    else:
        formulario = MovimientosForm()
        if formulario.validate():
            try:
                dbManager.modificaTablaSQL("UPDATE movimientos SET fecha = ?, concepto = ?, categoria = ?, esGasto = ?, cantidad = ? WHERE id = ?",
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