import psycopg2

try:
    conexion = psycopg2.connect(
        host="localhost",
        dbname="comercio",
        user="postgres",
        password="clpb761",
        port="5432"
    )
    print("¡Conexión exitosa a PostgreSQL!")
    conexion.close()
except Exception as error:
    print(f"Error al conectar: {error}")