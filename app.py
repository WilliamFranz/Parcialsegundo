from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para manejar sesiones

# Inicializamos la lista de productos en la sesión
@app.before_request
def inicializar_productos():
    if 'productos' not in session:
        session['productos'] = []

# Página principal: lista de productos
@app.route('/')
def index():
    return render_template('index.html', productos=session['productos'])

# Agregar un producto
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    nuevo_producto = {
        'id': str(uuid.uuid4()),  # Genera un id único para cada producto
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }
    # Agregar el producto a la lista en la sesión
    session['productos'].append(nuevo_producto)
    session.modified = True  # Marcamos la sesión como modificada para que Flask la actualice
    return redirect(url_for('index'))

# Eliminar un producto
@app.route('/eliminar/<id>')
def eliminar_producto(id):
    # Filtrar para eliminar el producto con el id proporcionado
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
