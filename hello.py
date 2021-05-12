from flask import Flask #se importa la clase Flask

app = Flask(__name__) #se crea una instancia de Flask - hay que meterle un nombre siempre

@app.route('/') #es un decorador que le va decir un determinado contenido a la ruta (luego vendran los atributos) '/' es el mas simple que puede usarse porque es la barra que va despues de una direccion web
def index(): #debajo de un decorador siempre hay una funcion
    return 'Hola,mundo!' #la funcion devuelve algo

@app.route('/adios')
def bye():
    return 'Hasta luego, cocodrilo'

