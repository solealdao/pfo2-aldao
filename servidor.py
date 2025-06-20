from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Crear la base de datos
with app.app_context():
    db.create_all()

# Ruta de bienvenida
@app.route('/tareas', methods=['GET'])
def tareas():
    return render_template_string("<h1>Bienvenido/a al sistema de tareas!</h1>")

# Ruta de registro
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()

    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if not usuario or not contraseña:
        return jsonify({'mensaje': 'Faltan usuario o contraseña'}), 400

    # Revisar si el usuario ya existe
    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    # Hashear la contraseña
    contraseña_hash = generate_password_hash(contraseña)

    nuevo_usuario = Usuario(usuario=usuario, contraseña=contraseña_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado exitosamente'})

# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()

    usuario = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if not usuario or not contraseña:
        return jsonify({'mensaje': 'Faltan usuario o contraseña'}), 400

    usuario_db = Usuario.query.filter_by(usuario=usuario).first()

    if usuario_db and check_password_hash(usuario_db.contraseña, contraseña):
        return jsonify({'mensaje': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401

# Ruta de crear tarea
@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    datos = request.get_json()

    usuario_nombre = datos.get('usuario')
    descripcion = datos.get('descripcion')

    if not usuario_nombre or not descripcion:
        return jsonify({'mensaje': 'Faltan usuario o descripción'}), 400

    usuario_db = Usuario.query.filter_by(usuario=usuario_nombre).first()
    if not usuario_db:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    nueva_tarea = Tarea(descripcion=descripcion, usuario_id=usuario_db.id)
    db.session.add(nueva_tarea)
    db.session.commit()

    return jsonify({'mensaje': 'Tarea agregada exitosamente'})

# Ruta de listar tarea por usuario
@app.route('/tareas/<usuario>', methods=['GET'])
def listar_tareas(usuario):
    usuario_db = Usuario.query.filter_by(usuario=usuario).first()
    if not usuario_db:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    tareas = Tarea.query.filter_by(usuario_id=usuario_db.id).all()
    lista_tareas = [{'id': t.id, 'descripcion': t.descripcion} for t in tareas]

    return jsonify({'usuario': usuario, 'tareas': lista_tareas})

if __name__ == '__main__':
    app.run(debug=True)
