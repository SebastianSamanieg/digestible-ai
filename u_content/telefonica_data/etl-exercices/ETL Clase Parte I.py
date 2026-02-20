#pip install pandas
#pip install sqlalchemy
#pip install mysql-connector-python
#pip install psycopg2

import pandas as pd
import mysql.connector
import psycopg2


############################# Parametros ########################
ruta=r'C:\Users\LEGION\Documents\BI'

################################################################
##################     1. Extraer        #######################
################################################################

############### 1.1. Extraer Ventas de Mysql ###############

conexion=mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='ventas'
)

# Extracción Categoría
consulta_sql="SELECT * FROM categoria"
df_categoria=pd.read_sql_query(consulta_sql,conexion)
#print(df_categoria)


# Extracción Producto
consulta_sql="SELECT * FROM producto"
df_producto=pd.read_sql_query(consulta_sql,conexion)
#print(df_producto)

# Extracción Vendedor
consulta_sql="SELECT * FROM vendedor"
df_vendedor=pd.read_sql_query(consulta_sql,conexion)
#print(df_vendedor)

# Extracción venta_producto
consulta_sql="SELECT * FROM venta_producto"
df_venta_producto=pd.read_sql_query(consulta_sql,conexion)
#print(df_venta_producto)

############### 1.2. Extraer Recursos humanos de Postgres ###############

# Parámetros de conexión
conn = psycopg2.connect(
    host="localhost",        
    port="5432",            
    database="postgres",
    user="postgres",
    password="1234"
)

# Crear un cursor para ejecutar consultas
cur = conn.cursor()
 
# Extracción regions
query = "SELECT * from regions;"
df_regions = pd.read_sql(query, conn)
#print(df_regions)

# Extracción countries
query = "SELECT * from countries;"
df_countries = pd.read_sql(query, conn)
#print(df_countries)

# Extracción locations
query = "SELECT * from locations;"
df_locations = pd.read_sql(query, conn)
#print(df_locations)

# Extracción departments
query = "SELECT * from departments;"
df_departments = pd.read_sql(query, conn)
#print(df_departments)

# Extracción employees
query = "SELECT * from employees;"
df_employees = pd.read_sql(query, conn)
#print(df_employees)

# Extracción jobs
query = "SELECT * from jobs;"
df_jobs = pd.read_sql(query, conn)
#print(df_jobs)

################################################################
##################     2. Transformar        ###################
################################################################

############### 2.1. Integrar información Mysql ###############
df_ventas=pd.merge(df_venta_producto,df_producto,how='inner',on='idProducto')
df_ventas=pd.merge(df_ventas,df_categoria,how='inner',on='idCategoria')
df_ventas=pd.merge(df_ventas,df_vendedor,how='inner',on='idVendedor')
df_ventas.rename(columns={'Nombre_x':'categoria','Nombre_y':'Nombre'},inplace=True)

df_ventas.to_excel(ruta+'\df_ventas.xlsx',index=False)


############### 2.2. Integrar información Postgres ###############
df_rh=pd.merge(df_regions,df_countries,how='inner',on='region_id')
df_rh=pd.merge(df_rh,df_locations,how='inner',on='country_id')
df_rh=pd.merge(df_rh,df_departments,how='inner',on='location_id')
df_rh=pd.merge(df_rh,df_employees,how='inner',on='department_id')

df_rh.to_excel(ruta+'\df_rh.xlsx',index=False)

################# 2.3 Integración de dataframes ####################
df_ventas['Cedula']=df_ventas['Cedula'].astype(str)
union=df_ventas.merge(df_rh, left_on='Cedula', right_on='identificacion',how='inner' )


union.to_excel(ruta+'/union.xlsx',index=False)
