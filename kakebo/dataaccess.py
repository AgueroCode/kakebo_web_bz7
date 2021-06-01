import sqlite3

class DBmanager():
    def __toDict__(self, cur):
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

        return resultado

    def consultaMuchasSQL(self, query, parametros=[]):
        #abrimos la conexion
        conexion = sqlite3.connect("movimientos.db")
        cur = conexion.cursor()
        
        #ejecutamos la consultad
        cur.execute(query, parametros)
        resultado = self.__toDict__(cur)
        conexion.close()
        return resultado
    
    def consultaUnaSQL(self, query, parametros=[]):
        resultado = self.consultaMuchasSQL(query, parametros)
        if len(resultado) > 0:
            return resultado[0]

    def modificaTablaSQL(self, query, parametros=[]):
        conexion = sqlite3.connect("movimientos.db")
        cur = conexion.cursor()

        cur.execute(query, parametros)

        conexion.commit() #esto fija el cambio en la base de datos, confirma el cambio
        conexion.close()
