from flask import Flask, render_template, request, redirect, flash
import controlador_movies

app = Flask(__name__)

"""
Definición de rutas
"""


@app.route("/agregar_movie")
def formulario_agregar_movie():
    return render_template("agregar_movie.html")


@app.route("/guardar_movie", methods=["POST"])
def guardar_movie():
    nombre = request.form["nombre"]
    director = request.form["director"]
    year = request.form["year"]
    controlador_movies.insertar_movie(nombre, director, year)
    return redirect("/movies")


@ app.route("/")
@ app.route("/movies")
def movies():
    movies = controlador_movies.obtener_movies()
    return render_template("movies.html", movies=movies)


@ app.route("/eliminar_movie", methods=["POST"])
def eliminar_movie():
    controlador_movies.eliminar_movie(request.form["id"])
    return redirect("/movies")


@ app.route("/formulario_editar_movie/<int:id>")
def editar_movie(id):
    # Obtener la movie por ID
    movie = controlador_movies.obtener_movie_por_id(id)
    return render_template("editar_movie.html", movie=movie)


@ app.route("/actualizar_movie", methods=["POST"])
def actualizar_movie():
    id = request.form["id"]
    nombre = request.form["nombre"]
    director = request.form["director"]
    year = request.form["year"]
    controlador_movies.actualizar_movie(nombre, director, year, id)
    return redirect("/movies")


# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
