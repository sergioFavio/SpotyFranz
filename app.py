# coding: utf-8
from flask import Flask, render_template, request, url_for,redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
        
app = Flask(__name__)
app.secret_key = 'cochabamba'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{clave}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        clave = '',
        #clave = 'admin',
        servidor = 'localhost',
        database = 'spotyfranz'
    )

db = SQLAlchemy(app)

class Canciones(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    idioma = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    clave = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def index():
    lista = Canciones.query.order_by(Canciones.id)
    return render_template('listar.html',titulo= 'Canciones', musicas=lista)


@app.route('/nuevoregistro')
def nuevoregistro():
    if session['usuario_logueado'] == None:
        flash('Usuario no conectado.')
        return redirect(url_for('login', proxima = url_for('nuevoregistro')))
    else:
        flash('Usuario conectado.') 
        return render_template('nuevoRegistro.html', titulo='Nueva Canción')


@app.route('/crear', methods=['POST',])
def crear():
    titulo = request.form['titulo']
    categoria = request.form['categoria']
    idioma = request.form['idioma']

    cancion = Canciones.query.filter_by(titulo=titulo).first()

    if cancion:
        flash('Esta canción ya existe!')
        return redirect(url_for('index'))

    nueva_cancion = Canciones(titulo=titulo, categoria=categoria, idioma=idioma)
    db.session.add(nueva_cancion)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['clave'] == usuario.clave:
            session['usuario_logueado'] = usuario.nickname
            flash(usuario.nickname + ' ¡conectado con éxito!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario no conectado.')
            return redirect(url_for('login', proxima = url_for('nuevoregistro')))
    else:
        flash('Usuario no conectado.')
        return redirect(url_for('login', proxima = url_for('nuevoregistro')))

    
@app.route('/logout')
def logout():
    session['usuario_logueado'] = None
    flash('¡Logout efectuado exitosamente!')
    return redirect(url_for('index'))


app.run(host="0.0.0.0", port=5000)