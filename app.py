from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos (SQLite en este ejemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de datos (una tabla de usuarios en este ejemplo)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Ruta para el formulario de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Verificar si el usuario ya existe en la base de datos
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            # El usuario ya existe, mostrar un mensaje de error
            return render_template('register.html', error='El nombre de usuario ya está en uso')

        # Crear un nuevo usuario
        new_user = User(username=username, password=password)

        # Guardar el nuevo usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()

        # Redirigir a una página de éxito después del registro
        return redirect(url_for('success'))

    # Si la solicitud es GET, simplemente mostrar el formulario de registro
    return render_template('register.html')

# Página de éxito después del registro
@app.route('/success')
def success():
    return "Registro exitoso"

if __name__ == '__main__':
    app.run(debug=True)


