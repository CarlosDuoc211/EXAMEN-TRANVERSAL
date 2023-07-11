import hashlib
import sqlite3
from flask import Flask, request

app = Flask(__name__)
database = 'usuarios.db'
conn = sqlite3.connect(database)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT, password_hash TEXT)')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        c.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, password_hash))
        conn.commit()
        
        return "Usuario registrado exitosamente."
    
    return '''
    <form method="POST" action="/registro">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre"><br>
        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password"><br>
        <input type="submit" value="Registrarse">
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        
        c.execute("SELECT password_hash FROM usuarios WHERE nombre=?", (nombre,))
        result = c.fetchone()
        
        if result is not None:
            stored_password_hash = result[0]
            entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if stored_password_hash == entered_password_hash:
                return "Inicio de sesión exitoso."
        
        return "Nombre de usuario o contraseña incorrectos."
    
    return '''
    <form method="POST" action="/login">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre"><br>
        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password"><br>
        <input type="submit" value="Iniciar sesión">
    </form>
    '''

if __name__ == '__main__':
    create_table()
    app.run(port=4850)
