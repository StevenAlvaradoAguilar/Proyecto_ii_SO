import psycopg2

def conexion():
    conexion = psycopg2.connect(host="localhost", database="Categorias", user="postgres", password="1234", port ="5432")
    return conexion



