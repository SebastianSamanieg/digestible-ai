# ═══════════════════════════════════════════════════════════════════════════════
# TALLER 1: Exploración y Preparación de Datos
# Predicción de Precios de Apartamentos en Bogotá
# Metodología: CRISP-DM
# ═══════════════════════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: ENTENDIMIENTO DEL NEGOCIO
# ─────────────────────────────────────────────────────────────────────────────
"""
Objetivo del negocio:
- Construir un modelo que prediga el precio de VENTA de apartamentos en Bogotá.
- Variable objetivo: precio_venta (COP)
- Decisiones apoyadas: tasación automatizada, comparación de mercado, inversión inmobiliaria.
- Éxito del modelo: RMSE y R² sobre el conjunto de prueba (20%).
- Restricciones: datos de una sola fuente (habi.co), agosto 2024.
"""

# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: ENTENDIMIENTO DE LOS DATOS (EDA)
# ─────────────────────────────────────────────────────────────────────────────

# Asumimos que df ya fue cargado y limpiado con el pipeline anterior
# df = obtener_datos()  # descomentar si se ejecuta desde cero

# ── PASO 1: FILTRADO — solo registros de VENTA ────────────────────────────────
print("=" * 70)
print("PASO 1: FILTRADO DEL DATASET — Solo registros de VENTA")
print("=" * 70)

df_venta = df[df['tipo_operacion'] == 'VENTA'].copy()

print(f"Registros totales:       {len(df):,}")
print(f"Registros de VENTA:      {len(df_venta):,}")
print(f"Registros eliminados:    {len(df) - len(df_venta):,}")
print(f"Registros sin precio:    {df_venta['precio_venta'].isna().sum():,}")

# Eliminar registros sin precio_venta (variable objetivo)
df_venta = df_venta.dropna(subset=['precio_venta'])
print(f"Dataset final para EDA:  {len(df_venta):,} registros")


# ── PASO 2: SELECCIÓN DE VARIABLES ────────────────────────────────────────────
print("\n" + "=" * 70)
print("PASO 2: SELECCIÓN DE VARIABLES")
print("=" * 70)

# Variables numéricas (7)
vars_numericas = [
    'precio_venta',           # Variable objetivo
    'area',                   # m² del apartamento
    'distancia_estacion_tm_m',# Distancia a TransMilenio
    'distancia_parque_m',     # Distancia al parque más cercano
]

# Columnas que necesitan conversión a numérico
cols_convertir = ['habitaciones', 'banos', 'parqueaderos', 'administracion']
for col in cols_convertir:
    df_venta[col] = pd.to_numeric(df_venta[col], errors='coerce')

vars_numericas += cols_convertir  # Total: 8 numéricas

# Variables categóricas (4)
vars_categoricas = [
    'localidad',              # Zona de la ciudad
    'antiguedad',             # Rango de antigüedad
    'estrato',                # Estrato socioeconómico
    'is_cerca_estacion_tm',   # Binaria: cerca de TM (0/1)
]

todas_las_vars = vars_numericas + vars_categoricas
df_sel = df_venta[todas_las_vars].copy()

print(f"Variables numéricas seleccionadas ({len(vars_numericas)}):")
for v in vars_numericas:
    print(f"  • {v}")

print(f"\nVariables categóricas seleccionadas ({len(vars_categoricas)}):")
for v in vars_categoricas:
    print(f"  • {v}")


# ── PASO 3.1: ESTRUCTURA DEL DATASET ─────────────────────────────────────────
print("\n" + "=" * 70)
print("PASO 3.1: ESTRUCTURA DEL DATASET")
print("=" * 70)

print(f"\nFilas:    {df_sel.shape[0]:,}")
print(f"Columnas: {df_sel.shape[1]}")
print("\nTipos de datos:")
print(df_sel.dtypes.to_string())


# ── PASO 3.2: VALORES NULOS ───────────────────────────────────────────────────
print("\n" + "=" * 70)
print("PASO 3.2: ANÁLISIS DE VALORES NULOS")
print("=" * 70)

nulos = df_sel.isnull().sum()
pct_nulos = (nulos / len(df_sel) * 100).round(2)
resumen_nulos = pd.DataFrame({
    'Nulos': nulos,
    '% Nulos': pct_nulos
}).sort_values('% Nulos', ascending=False)

print(resumen_nulos[resumen_nulos['Nulos'] > 0])
print(f"\n¿precio_venta tiene nulos? {df_sel['precio_venta'].isna().sum()} → Variable objetivo completa ✓")


# ── PASO 3.3: ANÁLISIS DE LA VARIABLE OBJETIVO ───────────────────────────────
print("\n" + "=" * 70)
print("PASO 3.3: VARIABLE OBJETIVO — precio_venta")
print("=" * 70)

precio = df_sel['precio_venta'].dropna()
print(f"\nEstadísticas descriptivas:")
print(precio.describe().apply(lambda x: f'{x:,.0f}'))
print(f"\nAsimetría (skewness): {precio.skew():.4f}")
print(f"Curtosis:             {precio.kurtosis():.4f}")

# La alta asimetría justifica transformación logarítmica
print(f"\n→ Asimetría > 1: se recomienda transformación LOG para normalizar distribución")
print(f"  log(precio_venta): skewness = {np.log(precio).skew():.4f}")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Análisis de la Variable Objetivo: precio_venta', fontsize=14, fontweight='bold')

# Distribución original
axes[0].hist(precio / 1e6, bins=60, color='steelblue', edgecolor='white', alpha=0.8)
axes[0].set_title('Distribución Original')
axes[0].set_xlabel('Precio (millones COP)')
axes[0].set_ylabel('Frecuencia')

# Distribución log-transformada
axes[1].hist(np.log(precio), bins=60, color='seagreen', edgecolor='white', alpha=0.8)
axes[1].set_title('Distribución Log-transformada')
axes[1].set_xlabel('log(Precio)')
axes[1].set_ylabel('Frecuencia')

# Boxplot con outliers
axes[2].boxplot(precio / 1e6, vert=True, patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[2].set_title('Boxplot — Outliers')
axes[2].set_ylabel('Precio (millones COP)')

plt.tight_layout()
plt.savefig('/home/claude/fig_precio_distribucion.png', dpi=130, bbox_inches='tight')
plt.close()
print("\n[Gráfico guardado: fig_precio_distribucion.png]")


# ── PASO 3.4: ANÁLISIS DE CORRELACIONES ──────────────────────────────────────
print("\n" + "=" * 70)
print("PASO 3.4: CORRELACIONES CON precio_venta")
print("=" * 70)

vars_corr = ['precio_venta', 'area', 'habitaciones', 'banos',
             'parqueaderos', 'administracion', 'distancia_estacion_tm_m', 'distancia_parque_m']

df_corr = df_sel[vars_corr].dropna()
corr_matrix = df_corr.corr()
corr_precio = corr_matrix['precio_venta'].drop('precio_venta').sort_values(ascending=False)

print("\nCorrelación de Pearson con precio_venta:")
for var, val in corr_precio.items():
    direccion = "positiva ↑" if val > 0.1 else ("negativa ↓" if val < -0.1 else "débil  →")
    print(f"  {var:<30} {val:+.4f}  [{direccion}]")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Análisis de Correlaciones', fontsize=14, fontweight='bold')

# Heatmap
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, ax=axes[0], annot=True, fmt='.2f', cmap='coolwarm',
            mask=mask, vmin=-1, vmax=1, linewidths=0.5)
axes[0].set_title('Mapa de Correlaciones')

# Bar chart correlaciones con precio
colors = ['steelblue' if v > 0 else 'tomato' for v in corr_precio.values]
axes[1].barh(corr_precio.index, corr_precio.values, color=colors, edgecolor='white')
axes[1].axvline(0, color='black', linewidth=0.8)
axes[1].set_title('Correlación con precio_venta')
axes[1].set_xlabel('Coeficiente de Pearson')

plt.tight_layout()
plt.savefig('/home/claude/fig_correlaciones.png', dpi=130, bbox_inches='tight')
plt.close()
print("\n[Gráfico guardado: fig_correlaciones.png]")


# ── PASO 3.5: DETECCIÓN DE OUTLIERS ──────────────────────────────────────────
print("\n" + "=" * 70)
print("PASO 3.5: DETECCIÓN DE OUTLIERS (Método IQR)")
print("=" * 70)

def detectar_outliers_iqr(serie, nombre):
    Q1 = serie.quantile(0.25)
    Q3 = serie.quantile(0.75)
    IQR = Q3 - Q1
    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR
    outliers = serie[(serie < limite_inf) | (serie > limite_sup)]
    pct = len(outliers) / len(serie) * 100
    print(f"  {nombre:<30} {len(outliers):>5} outliers ({pct:.1f}%)")
    return limite_inf, limite_sup

print("\nOutliers detectados por variable:")
vars_outlier = ['precio_venta', 'area', 'administracion', 'distancia_estacion_tm_m']
limites = {}
for v in vars_outlier:
    s = df_sel[v].dropna()
    limites[v] = detectar_outliers_iqr(s, v)

fig, axes = plt.subplots(1, 4, figsize=(18, 5))
fig.suptitle('Detección de Outliers por Variable', fontsize=14, fontweight='bold')
for i, v in enumerate(vars_outlier):
    axes[i].boxplot(df_sel[v].dropna(), patch_artist=True,
                    boxprops=dict(facecolor='steelblue', alpha=0.6),
                    flierprops=dict(marker='o', color='tomato', markersize=3))
    axes[i].set_title(v, fontsize=9)
    axes[i].set_ylabel('Valor')

plt.tight_layout()
plt.savefig('/home/claude/fig_outliers.png', dpi=130, bbox_inches='tight')
plt.close()
print("\n[Gráfico guardado: fig_outliers.png]")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: PREPARACIÓN DE LOS DATOS
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("FASE 3: PREPARACIÓN DE LOS DATOS")
print("=" * 70)


# ── 3.1 LIMPIEZA ─────────────────────────────────────────────────────────────
print("\n── 3.1 Limpieza de datos")

df_prep = df_sel.copy()

# Imputación de nulos con mediana (variables numéricas)
vars_num_imputar = ['habitaciones', 'banos', 'parqueaderos',
                    'administracion', 'distancia_estacion_tm_m', 'distancia_parque_m']

for col in vars_num_imputar:
    mediana = df_prep[col].median()
    nulos_antes = df_prep[col].isna().sum()
    df_prep[col] = df_prep[col].fillna(mediana)
    if nulos_antes > 0:
        print(f"  Imputados {nulos_antes:,} nulos en '{col}' con mediana={mediana:.2f}")

# Imputación de categóricas con moda
vars_cat_imputar = ['localidad', 'antiguedad', 'estrato']
for col in vars_cat_imputar:
    moda = df_prep[col].mode()[0]
    nulos_antes = df_prep[col].isna().sum()
    df_prep[col] = df_prep[col].fillna(moda)
    if nulos_antes > 0:
        print(f"  Imputados {nulos_antes:,} nulos en '{col}' con moda='{moda}'")

# Eliminación de outliers extremos en precio_venta (>99.5 percentil)
p995 = df_prep['precio_venta'].quantile(0.995)
p005 = df_prep['precio_venta'].quantile(0.005)
antes = len(df_prep)
df_prep = df_prep[(df_prep['precio_venta'] >= p005) & (df_prep['precio_venta'] <= p995)]
print(f"\n  Outliers extremos de precio eliminados: {antes - len(df_prep):,} registros")
print(f"  Dataset tras limpieza: {len(df_prep):,} registros")

# Verificar duplicados
dupl = df_prep.duplicated().sum()
print(f"  Duplicados encontrados: {dupl}")


# ── 3.2 TRANSFORMACIÓN LOG + ESCALADO ────────────────────────────────────────
print("\n── 3.2 Escalado de variables numéricas")

# Aplicar log a precio_venta
df_prep['log_precio_venta'] = np.log(df_prep['precio_venta'])

vars_escalar = ['area', 'habitaciones', 'banos', 'parqueaderos',
                'administracion', 'distancia_estacion_tm_m', 'distancia_parque_m']

# StandardScaler: estandariza a media=0, desv=1
# Justificación: al usar modelos lineales o regularizados (Ridge, Lasso),
# StandardScaler es preferido sobre MinMax porque es robusto ante outliers
# y mantiene la forma de la distribución.
scaler = StandardScaler()
df_prep[vars_escalar] = scaler.fit_transform(df_prep[vars_escalar])

print(f"  Técnica seleccionada: StandardScaler")
print(f"  Justificación: adecuado para modelos lineales/regularizados,")
print(f"  robusto ante outliers residuales tras limpieza.")
print(f"  Variables escaladas: {vars_escalar}")


# ── 3.3 CODIFICACIÓN — One-Hot Encoding ──────────────────────────────────────
print("\n── 3.3 Codificación de variables categóricas (One-Hot Encoding)")

# Justificación: las variables categóricas no tienen orden inherente
# (localidad, antigüedad). OHE crea columnas binarias sin introducir
# relaciones ordinales artificiales.

vars_ohe = ['localidad', 'antiguedad', 'estrato']
df_encoded = pd.get_dummies(df_prep, columns=vars_ohe, drop_first=False, dtype=int)

# is_cerca_estacion_tm ya es binaria (0/1), no necesita OHE
print(f"  Variables codificadas: {vars_ohe}")
print(f"  Columnas antes del OHE: {df_prep.shape[1]}")
print(f"  Columnas después del OHE: {df_encoded.shape[1]}")


# ── 3.4 DIVISIÓN TRAIN / TEST ─────────────────────────────────────────────────
print("\n── 3.4 División del dataset (80% entrenamiento / 20% prueba)")

# Features (X) y variable objetivo (y)
# Usamos log_precio_venta para normalizar la distribución del target
X = df_encoded.drop(columns=['precio_venta', 'log_precio_venta'])
y = df_encoded['log_precio_venta']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

print(f"\n  Total de muestras:   {len(X):,}")
print(f"  Entrenamiento (80%): {len(X_train):,}")
print(f"  Prueba       (20%): {len(X_test):,}")
print(f"  Features totales:   {X.shape[1]}")
print(f"\n  Justificación: la separación permite evaluar la generalización del")
print(f"  modelo sobre datos no vistos. random_state=42 asegura reproducibilidad.")


# ── RESUMEN FINAL ─────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("RESUMEN FINAL DEL DATASET PREPARADO")
print("=" * 70)
print(f"  Registros finales:          {len(df_encoded):,}")
print(f"  Features para modelado:     {X.shape[1]}")
print(f"  Variable objetivo:          log(precio_venta)")
print(f"  Nulos en X_train:           {X_train.isna().sum().sum()}")
print(f"  Nulos en X_test:            {X_test.isna().sum().sum()}")
print(f"  Dataset listo para modelado ✓")
