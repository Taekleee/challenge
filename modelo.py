import importlib.machinery
import importlib.util
from flask import jsonify

# Import mymodule
loader = importlib.machinery.SourceFileLoader( 'db', 'db.py' )
spec = importlib.util.spec_from_loader( 'db', loader )
db = importlib.util.module_from_spec( spec )
loader.exec_module( db )

def mensaje_exito():
    mensaje = "Operación exitosa"
    response = {
        "status": "success",
        "message": mensaje
    }
    return response


def obtener_registros(region, coordenadas):
    con = db.conexion()
    registros = []
    print(coordenadas)
    wkt_polygon = "POLYGON(("
    for coordenada in coordenadas:
        wkt_polygon += f"{coordenada['longitude']} {coordenada['latitude']},"
    wkt_polygon = wkt_polygon.rstrip(",") + "))"
    print(wkt_polygon)
    with con.cursor() as cursor:
        cursor.execute("SELECT MIN(`datetime`), MAX(`datetime`), COUNT(*) FROM trips WHERE ST_CONTAINS(ST_GeomFromText(%s), origin_coord) AND ST_CONTAINS(ST_GeomFromText(%s), destination_coord) AND region = %s GROUP BY WEEK(`datetime`);", (wkt_polygon, wkt_polygon, region,))
    registros = cursor.fetchall()
    con.close()
    return registros


def insertar_registro(region, origin, destination, datetime, datasource):
    con = db.conexion()
    registros = []
    with con.cursor() as cursor:
        cursor.execute("INSERT INTO trips(region, origin_coord, destination_coord, datetime, datasource) VALUES (%s, ST_GeomFromText(%s), ST_GeomFromText(%s), %s, %s)", (region,origin, destination, datetime, datasource,))
    con.commit()
    con.close()
    
    return registros


