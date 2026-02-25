import kagglehub
import pandas as pd
import os

# 1️⃣ Descargar dataset
path = kagglehub.dataset_download("sadiajavedd/social-media-user-activity-dataset")

print("Path to dataset files:", path)

# 2️⃣ Buscar automáticamente el archivo CSV dentro de la carpeta descargada
files = os.listdir(path)
csv_files = [f for f in files if f.endswith(".csv")]

if not csv_files:
    raise FileNotFoundError("No se encontró ningún archivo CSV en el dataset.")

csv_path = os.path.join(path, csv_files[0])
print("Archivo encontrado:", csv_path)

# 3️⃣ Cargar dataset
df = pd.read_csv(csv_path)

# 4️⃣ Mostrar información general
print("\n🔹 Primeras 5 filas:")
print(df.head())

print("\n🔹 Columnas del dataset:")
print(df.columns.tolist())

print("\n🔹 Tipos de datos:")
print(df.dtypes)

print("\n🔹 Información general (info):")
print(df.info())

print("\n🔹 Resumen estadístico (numérico):")
print(df.describe())

print("\n🔹 Resumen estadístico (incluyendo categóricas):")
print(df.describe(include="all"))

print("\n🔹 Valores nulos por columna:")
print(df.isnull().sum())