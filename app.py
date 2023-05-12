from flask import Flask, render_template, request, url_for

class Cancion:
    def __init__(self, titulo, categoria, idioma):
        self.titulo = titulo
        self.categoria = categoria
        self.idioma = idioma

cancion1= Cancion('La guitarra', 'Pop', 'Castellano')
cancion2= Cancion('Para no verte más', 'Pop', 'Castellano')
cancion3= Cancion('Balada para un gordo', 'Balada', 'Castellano')
lista=[cancion1, cancion2, cancion3]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('listar.html',titulo= 'Canciones', musicas=lista)


@app.route('/nuevoregistro')
def nuevoregistro():
    return render_template('nuevoRegistro.html', titulo='Nueva Canción')

@app.route('/crear', methods=['POST',])
def crear():
    titulo = request.form['titulo']
    categoria = request.form['categoria']
    idioma = request.form['idioma']
    cancion = Cancion(titulo, categoria, idioma)
    lista.append(cancion)
    return redirect('/')



app.run(host="0.0.0.0", port=5000)