"""
Módulo: Embeddings con modelo LOCAL
Descripción: Calcula similitud semántica usando modelo descargado manualmente
Autor: JSSAMANIEGPO
Fecha: 2025-02-09
"""

# ============================================================================
# IMPORTS
# ============================================================================
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
import os

# ============================================================================
# CONFIGURACIÓN - Ruta del modelo local (SIN subcarpeta)
# ============================================================================
# Los archivos están directamente en models/, no en una subcarpeta
MODEL_PATH = r"C:\Users\JSSAMANIEGPO\PycharmProjects\llm-learning-resources\models"

# Verificar que el modelo existe
if not os.path.exists(os.path.join(MODEL_PATH, "config.json")):
    print(f"❌ Error: No se encuentra config.json en {MODEL_PATH}")
    exit(1)

if not os.path.exists(os.path.join(MODEL_PATH, "pytorch_model.bin")):
    print(f"❌ Error: No se encuentra pytorch_model.bin en {MODEL_PATH}")
    exit(1)

print("=" * 70)
print("CARGANDO MODELO LOCAL")
print("=" * 70)
print(f"Ruta: {MODEL_PATH}")
print("\nArchivos encontrados:")
print(f"  ✓ config.json")
print(f"  ✓ pytorch_model.bin ({os.path.getsize(os.path.join(MODEL_PATH, 'pytorch_model.bin')) / 1024 / 1024:.0f} MB)")
print(f"  ✓ tokenizer_config.json")

# ============================================================================
# INICIALIZAR EMBEDDINGS (desde modelo local)
# ============================================================================
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_PATH,  # Apuntar directamente a la carpeta models
    model_kwargs={
        'device': 'cpu',
        'local_files_only': True  # No buscar en internet
    },
    encode_kwargs={
        'normalize_embeddings': True
    }
)

print("\n✓ Modelo cargado correctamente desde disco local")

# ============================================================================
# USAR (Igual que con Azure)
# ============================================================================
print("\n" + "=" * 70)
print("GENERANDO EMBEDDINGS")
print("=" * 70)

texto1 = "La capital de Francia es París"
texto2 = "París es la ciudad capital de Francia"
texto3 = "El Sol es una estrella"

vec1 = embeddings.embed_query(texto1)
vec2 = embeddings.embed_query(texto2)
vec3 = embeddings.embed_query(texto3)

print(f"✓ Embeddings generados")
print(f"Dimensión: {len(vec1)}")
print(f"Dimensión: {len(vec2)}")
print(f"Dimensión: {len(vec3)}")

# ============================================================================
# CALCULAR SIMILITUDES
# ============================================================================
print("\n" + "=" * 70)
print("SIMILITUDES COSENO")
print("=" * 70)

cos_sim_1_2 = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
cos_sim_1_3 = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))
cos_sim_2_3 = np.dot(vec2, vec3) / (np.linalg.norm(vec2) * np.linalg.norm(vec3))

print(f"\nTexto 1: '{texto1}'")
print(f"Texto 2: '{texto2}'")
print(f"Texto 3: '{texto3}'")

print("\n" + "-" * 70)
print(f"Similitud 1 ↔ 2: {cos_sim_1_2:.4f} → Misma semántica (Francia-París)")
print(f"Similitud 1 ↔ 3: {cos_sim_1_3:.4f} → Diferente semántica (Francia vs Sol)")
print(f"Similitud 2 ↔ 3: {cos_sim_2_3:.4f} → Diferente semántica (París vs Sol)")
print("=" * 70)