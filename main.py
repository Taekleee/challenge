import importlib.machinery
import importlib.util
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

# Import modulo
loader = importlib.machinery.SourceFileLoader( 'modelo', 'modelo.py' )
spec = importlib.util.spec_from_loader( 'modelo', loader )
modelo = importlib.util.module_from_spec( spec )
loader.exec_module( modelo )


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mypassword'
socketio = SocketIO(app)


# Enpoint para obtener los viajes según los parámetros ingresados
@app.route("/tripsByBounding", methods=["POST"])
def get_user():
    resultados = []
    region = request.json['region']
    coordenadas = request.json['coordenadas']

    result = modelo.obtener_registros(region, coordenadas)
    claves = ['Día inicial', 'Día final', 'Cantidad de viajes']
    for objetos in result:
        list2dic = dict(zip(claves, objetos)) 
        resultados.append(list2dic)

    return jsonify({"data":resultados})


# Enpoint para insertar datos nuevos
@app.route("/insertData", methods=["POST"])
def insertData():
    region = request.json['region']
    origin = request.json['origin']
    destination = request.json['destination']
    datetime = request.json['datetime']
    datasource = request.json['datasource']
    modelo.insertar_registro(region, origin, destination, datetime, datasource)

    User_dict = {
        "region": region,
        "origin": origin,
        "destination":  destination,
        "datetime": datetime,
        "datasource": datasource
    }
    enviar_actualizacion_a_clientes("datos")
    return jsonify(modelo.mensaje_exito())

#Conexión para websocket
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado: ', request.sid)

#emit del websocket
def enviar_actualizacion_a_clientes(mensaje):
    socketio.emit('actualizacion', {'respuesta': f'Hola, se agregó un dato: {mensaje}'}) 
     
if __name__ == '__main__':
  with app.app_context():
    socketio.run(app)
    app.run(host="localhost", port="5000", debug=True)
    