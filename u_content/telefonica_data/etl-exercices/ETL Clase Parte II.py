import os
import sqlite3
import pandas as pd

############################# Parametros ########################
ruta=r'C:\Users\JSSAMANIEGPO\PycharmProjects\etl-exercices\data'

union=pd.read_excel(ruta+'/union.xlsx')

################# 2.4.Creación de dimensiones #########################

############################# Ejercicio 1 ########################
# Realizar comentarios en cada línea que explique que esta haciendo cada parte del código

# Muestra información general del DataFrame 'union', como tipos de datos, valores no nulos y memoria utilizada
union.info()

# Crea un DataFrame para la dimensión Producto seleccionando solo las columnas relevantes
df_producto = union[['idProducto', 'Marca', 'Modelo', 'categoria']]
# Elimina filas duplicadas para obtener una lista única de productos
df_producto = df_producto.drop_duplicates()

# Crea un DataFrame para la dimensión Ubicación seleccionando solo las columnas relevantes
df_ubicacion = union[['location_id', 'city', 'country_name', 'region_name']]
# Elimina filas duplicadas para obtener una lista única de ubicaciones
df_ubicacion = df_ubicacion.drop_duplicates()
# Renombra las columnas para mejorar la legibilidad y estandarizar los nombres
df_ubicacion = df_ubicacion.rename(columns={'location_id': 'idUbicacion',
                                           'city': 'Ciudad',
                                           'country_name': 'Pais'
                                           })

# Crea un DataFrame para la dimensión Empleado seleccionando solo las columnas relevantes
df_empleado = union[['employee_id', 'first_name', 'last_name', 'identificacion']]
# Elimina filas duplicadas para obtener una lista única de empleados
df_empleado = df_empleado.drop_duplicates()
# Renombra las columnas para mejorar la legibilidad y estandarizar los nombres
df_empleado = df_empleado.rename(columns={'employee_id': 'idVendedor',
                                         'first_name': 'Nombre',
                                         'last_name': 'Apellido'
                                         })

# Crea una nueva columna 'id_fecha' asignando un identificador único a cada fecha de venta
# pd.factorize() convierte valores únicos a enteros (0, 1, 2...) y retorna dos valores:
# los códigos y las etiquetas únicas correspondientes. Aquí se toma solo el primer valor (los códigos)
union['id_fecha'] = pd.factorize(union['Fecha_Venta'])[0]

# Crea un DataFrame para la dimensión Tiempo seleccionando solo las columnas relevantes
df_tiempo = union[['id_fecha', 'Fecha_Venta']]
# Elimina filas duplicadas para obtener una lista única de fechas
df_tiempo = df_tiempo.drop_duplicates()

# Convierte la columna 'Fecha_Venta' al tipo datetime para poder extraer componentes de fecha
df_tiempo['Fecha_Venta'] = pd.to_datetime(df_tiempo['Fecha_Venta'])
# Extrae el año de cada fecha y lo guarda en una nueva columna
df_tiempo['anio'] = df_tiempo['Fecha_Venta'].dt.year
# Extrae el mes de cada fecha y lo guarda en una nueva columna
df_tiempo['mes'] = df_tiempo['Fecha_Venta'].dt.month
# Extrae el día de cada fecha y lo guarda en una nueva columna
df_tiempo['dia'] = df_tiempo['Fecha_Venta'].dt.day

# Crea la tabla de hechos (fact table) seleccionando las columnas clave y las métricas
df_fact = union[['idVenta', 'idProducto', 'location_id', 'employee_id', 'id_fecha', 'Valor']]
# Renombra las columnas para mejorar la legibilidad y estandarizar los nombres
df_fact = df_fact.rename(columns={'idVenta': 'idFact',
                                'location_id': 'idUbicacion',
                                'employee_id': 'idVendedor',
                                'Valor': 'Ventas'})

###################################################################
############### CARGA (L) #########################################

############################## Ejercicio 2 ##########################################
###Completar el Script para cargar la información a una base de datos en sqlite en la ruta: C:\Users\JSSAMANIEGPO\PycharmProjects\etl-exercices\sqlite  llamada dwh (Datawarehouse) ####

import os
import sqlite3
import pandas as pd

# Definir la ruta de la base de datos SQLite
db_directory = r"C:\Users\JSSAMANIEGPO\PycharmProjects\etl-exercices\sqlite"
db_path = os.path.join(db_directory, "dwh.db")

# Crear el directorio si no existe
if not os.path.exists(db_directory):
    os.makedirs(db_directory)
    print(f"Directorio creado: {db_directory}")

# Conectar a la base de datos SQLite (se creará si no existe)
print(f"Conectando a la base de datos: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Función para crear tablas si no existen
def crear_tablas():
    # Crear tabla de dimensión Producto
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS dim_producto
                   (
                       idProducto
                       INTEGER
                       PRIMARY
                       KEY,
                       Marca
                       TEXT,
                       Modelo
                       TEXT,
                       categoria
                       TEXT
                   )
                   ''')

    # Crear tabla de dimensión Ubicación
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS dim_ubicacion
                   (
                       idUbicacion
                       INTEGER
                       PRIMARY
                       KEY,
                       Ciudad
                       TEXT,
                       Pais
                       TEXT,
                       region_name
                       TEXT
                   )
                   ''')

    # Crear tabla de dimensión Empleado/Vendedor
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS dim_vendedor
                   (
                       idVendedor
                       INTEGER
                       PRIMARY
                       KEY,
                       Nombre
                       TEXT,
                       Apellido
                       TEXT,
                       identificacion
                       TEXT
                   )
                   ''')

    # Crear tabla de dimensión Tiempo
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS dim_tiempo
                   (
                       id_fecha
                       INTEGER
                       PRIMARY
                       KEY,
                       Fecha_Venta
                       TEXT,
                       anio
                       INTEGER,
                       mes
                       INTEGER,
                       dia
                       INTEGER
                   )
                   ''')

    # Crear tabla de hechos (fact table)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS fact_ventas
                   (
                       idFact
                       INTEGER
                       PRIMARY
                       KEY,
                       idProducto
                       INTEGER,
                       idUbicacion
                       INTEGER,
                       idVendedor
                       INTEGER,
                       id_fecha
                       INTEGER,
                       Ventas
                       REAL,
                       FOREIGN
                       KEY
                   (
                       idProducto
                   ) REFERENCES dim_producto
                   (
                       idProducto
                   ),
                       FOREIGN KEY
                   (
                       idUbicacion
                   ) REFERENCES dim_ubicacion
                   (
                       idUbicacion
                   ),
                       FOREIGN KEY
                   (
                       idVendedor
                   ) REFERENCES dim_vendedor
                   (
                       idVendedor
                   ),
                       FOREIGN KEY
                   (
                       id_fecha
                   ) REFERENCES dim_tiempo
                   (
                       id_fecha
                   )
                       )
                   ''')

    conn.commit()
    print("Tablas creadas correctamente")


# Función para insertar datos en las tablas
def cargar_datos():
    # Cargar datos en la tabla de dimensión Producto
    df_producto.to_sql('dim_producto', conn, if_exists='replace', index=False)
    print(f"Datos insertados en dim_producto: {len(df_producto)} registros")

    # Cargar datos en la tabla de dimensión Ubicación
    df_ubicacion.to_sql('dim_ubicacion', conn, if_exists='replace', index=False)
    print(f"Datos insertados en dim_ubicacion: {len(df_ubicacion)} registros")

    # Cargar datos en la tabla de dimensión Empleado/Vendedor
    df_empleado.to_sql('dim_vendedor', conn, if_exists='replace', index=False)
    print(f"Datos insertados en dim_vendedor: {len(df_empleado)} registros")

    # Cargar datos en la tabla de dimensión Tiempo
    df_tiempo.to_sql('dim_tiempo', conn, if_exists='replace', index=False)
    print(f"Datos insertados en dim_tiempo: {len(df_tiempo)} registros")

    # Cargar datos en la tabla de hechos
    df_fact.to_sql('fact_ventas', conn, if_exists='replace', index=False)
    print(f"Datos insertados en fact_ventas: {len(df_fact)} registros")

    conn.commit()


# Función para verificar la carga de datos
def verificar_carga():
    # Verificar datos en cada tabla
    tablas = ['dim_producto', 'dim_ubicacion', 'dim_vendedor', 'dim_tiempo', 'fact_ventas']

    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        print(f"Tabla {tabla}: {count} registros")

    # Ejecutar una consulta de prueba
    print("\nEjecutando consulta de prueba...")
    query = '''
            SELECT p.Marca, \
                   p.Modelo, \
                   u.Ciudad, \
                   u.Pais, \
                   t.anio, \
                   t.mes, \
                   SUM(f.Ventas) as Total_Ventas
            FROM fact_ventas f
                     JOIN dim_producto p ON f.idProducto = p.idProducto
                     JOIN dim_ubicacion u ON f.idUbicacion = u.idUbicacion
                     JOIN dim_tiempo t ON f.id_fecha = t.id_fecha
            GROUP BY p.Marca, p.Modelo, u.Ciudad, u.Pais, t.anio, t.mes
            ORDER BY Total_Ventas DESC LIMIT 5 \
            '''

    try:
        resultado = pd.read_sql_query(query, conn)
        print("Top 5 combinaciones por ventas:")
        print(resultado)
    except Exception as e:
        print(f"Error al ejecutar consulta de prueba: {e}")


# Ejecutar funciones
try:
    print("Iniciando carga de datos al Data Warehouse...")
    crear_tablas()
    cargar_datos()
    verificar_carga()
    print("Proceso completado exitosamente")
except Exception as e:
    print(f"Error durante la carga de datos: {e}")
finally:
    # Cerrar conexión a la base de datos
    cursor.close()
    conn.close()
    print("Conexión a la base de datos cerrada")

