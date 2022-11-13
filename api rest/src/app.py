from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config
# from validaciones import *

app = Flask(__name__)
conexion = MySQL(app)


@app.route('/movies', methods=['GET'])
def listar_movies():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, nombre, director, year FROM movies"
        cursor.execute(sql)
        datos = cursor.fetchall()
        movies = []
        for fila in datos:
            movie = {'id': fila[0], 'nombre': fila[1],
                     'director': fila[2], 'year': fila[3]}
            movies.append(movie)
        return jsonify({'movies': movies, 'mensaje': "Lista de peliculas.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_movies_bd(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, nombre, director, year FROM movies WHERE id = {0}".format(
            id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            movie = {'id': datos[0], 'nombre': datos[1],
                     'director': datos[2], 'year': datos[3]}
            return movie
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/movies/<id>', methods=['GET'])
def leer_movie(id):
    try:
        movie = leer_movies_bd(id)
        if movie != None:
            return jsonify({'movie': movie, 'mensaje': "Pelicula encontrada.", 'exito': True})
        else:
            return jsonify({'mensaje': "Pelicula no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/movies', methods=['POST'])
def registrar_movie():
    # print(request.json)
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO movies (nombre, director, year)
        VALUES ( '{0}', '{1}', {2})""".format(request.json['nombre'],
                                              request.json['director'], request.json['year'])
        cursor.execute(sql)
        # Confirma la acción de inserción.
        conexion.connection.commit()
        return jsonify({'mensaje': "Pelicula agregada.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/movies/<id>', methods=['PUT'])
def actualizar_movie(id):
    try:
        movie = leer_movies_bd(id)
        if movie != None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE movies SET nombre = '{0}', director = '{1}', year = {2}
            WHERE id = {3}""".format(request.json['nombre'], request.json['director'], request.json['year'], id)
            cursor.execute(sql)
            # Confirma la acción de actualización.
            conexion.connection.commit()
            return jsonify({'mensaje': "Pelicula actualizada.", 'exito': True})
            print(sql)
        else:
            return jsonify({'mensaje': "Pelicula no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/movies/<id>', methods=['DELETE'])
def eliminar_movie(id):
    try:
        movie = leer_movies_bd(id)
        if movie != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM movies WHERE id = '{0}'".format(id)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Pelicula eliminada.", 'exito': True})
        else:
            return jsonify({'mensaje': "pelicula no encontrada.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
