
from bd import conn_myslq


def insertar_movie(nombre, director, year):
    conexion = conn_myslq()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO movies(nombre, director, year) VALUES (%s, %s, %s)",
                       (nombre, director, year))
    conexion.commit()
    conexion.close()


def obtener_movies():
    conexion = conn_myslq()
    movies = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, director, year FROM movies.movies")
        movies = cursor.fetchall()
    conexion.close()
    return movies


def eliminar_movie(id):
    conexion = conn_myslq()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM movies WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_movie_por_id(id):
    conexion = conn_myslq()
    movie = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, director, year FROM movies WHERE id = %s", (id,))
        movie = cursor.fetchone()
    conexion.close()
    return movie


def actualizar_movie(nombre, director, year, id):
    conexion = conn_myslq()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE movies SET nombre = %s, director = %s, year = %s WHERE id = %s",
                       (nombre, director, year, id))
    conexion.commit()
    conexion.close()
