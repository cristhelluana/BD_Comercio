import psycopg2

class GestorAlumnos:
    """Clase que agrupa todas las operaciones sobre la tabla alumnos."""

    # -- Constructor: se conecta a la base al crear el objeto --
    def __init__(self, host, port, dbname, user, password):
        self.conexion = psycopg2.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
        self.cursor = self.conexion.cursor()
        print("Conexion exitosa a la base de datos")

    # -- CREATE: insertar un alumno nuevo --
    def crear(self, nombre, cedula, carrera, promedio):
        try:
            self.cursor.execute(
                "INSERT INTO alumnos (nombre, cedula, carrera, promedio) VALUES (%s, %s, %s, %s)",
                (nombre, cedula, carrera, promedio)
            )
            self.conexion.commit()
            print(f"Alumno '{nombre}' insertado correctamente.")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("No se pudo insertar el alumno:", e)

    # -- READ: listar todos los alumnos --
    def listar(self):
        self.cursor.execute(
            "SELECT id_alumno, nombre, cedula, carrera, promedio FROM alumnos ORDER BY id_alumno"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay alumnos cargados.")
            return
        print(f"{'ID':<4}{'Nombre':<22}{'Cédula':<15}{'Carrera':<32}{'Promedio':<8}")
        print("-" * 81)
        for f in filas:
            # Convertimos el promedio a string formateado para que luzca prolijo
            prom = f"{f[4]:.2f}" if f[4] is not None else "N/A"
            print(f"{f[0]:<4}{f[1]:<22}{f[2]:<15}{f[3]:<32}{prom:<8}")

    # -- UPDATE: modificar la carrera o promedio de un alumno --
    def modificar(self, id_alumno, nueva_carrera, nuevo_promedio):
        try:
            self.cursor.execute(
                "UPDATE alumnos SET carrera = %s, promedio = %s WHERE id_alumno = %s",
                (nueva_carrera, nuevo_promedio, id_alumno)
            )
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                print(f"Alumno actualizado ({self.cursor.rowcount} fila modificada)")
            else:
                print("No se encontro ningun alumno con ese ID.")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("No se pudo actualizar el alumno:", e)

    # --borrar un alumno --
    def borrar(self, id_alumno):
        try:
            self.cursor.execute(
                "DELETE FROM alumnos WHERE id_alumno = %s",
                (id_alumno,)
            )
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                print(f"Alumno borrado ({self.cursor.rowcount} fila eliminada)")
            else:
                print("No se encontro ningun alumno con ese ID.")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("No se pudo borrar el alumno:", e)

    # -- Cerrar la conexion --
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        print("Conexion cerrada. Hasta luego!")

# ------------------------------------------------------------
# Funcion que muestra el menu de opciones
# ------------------------------------------------------------
def mostrar_menu():
    print("\n===== GESTION DE ALUMNOS =====")
    print("1. Agregar alumno")
    print("2. Listar alumnos")
    print("3. Modificar datos de un alumno")
    print("4. Borrar alumno")
    print("5. Salir")
    print("===============================")

# ------------------------------------------------------------
# Programa principal
# ------------------------------------------------------------
def main():
    # Creamos el objeto gestor (se conecta a la base)
    # Recordá actualizar 'dbname' y 'password' con tus credenciales reales
    gestor = GestorAlumnos(
        host="localhost",
        port=5432,
        dbname="alumnos",
        user="postgres",
        password="clpb761"
    )

    while True:
        mostrar_menu()
        opcion = input("Elija una opcion (1-5): ")

        if opcion == "1":
            nombre = input("Nombre: ")
            cedula = input("Cédula: ")
            carrera = input("Carrera: ")
            try:
                promedio = float(input("Promedio (ej. 8.50): "))
                gestor.crear(nombre, cedula, carrera, promedio)
            except ValueError:
                print("Por favor, ingrese un valor numérico válido para el promedio.")

        elif opcion == "2":
            gestor.listar()

        elif opcion == "3":
            try:
                id_alumno = int(input("ID del alumno a modificar: "))
                nueva_carrera = input("Nueva carrera: ")
                nuevo_promedio = float(input("Nuevo promedio: "))
                gestor.modificar(id_alumno, nueva_carrera, nuevo_promedio)
            except ValueError:
                print("Por favor, ingrese valores válidos (ID numérico y promedio numérico).")

        elif opcion == "4":
            try:
                id_alumno = int(input("ID del alumno a borrar: "))
                gestor.borrar(id_alumno)
            except ValueError:
                print("Por favor, ingrese un ID numérico válido.")

        elif opcion == "5":
            gestor.cerrar()
            break

        else:
            print("Opción inválida. Intente de nuevo.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()