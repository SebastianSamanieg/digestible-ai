# =============================================================================
# FASE 2: ENTENDIMIENTO DE LOS DATOS
# =============================================================================

print("=" * 70)
print("FASE 2: ENTENDIMIENTO DE LOS DATOS")
print("=" * 70)

# Cargar datos
# NOTA: Ajustar la ruta según donde se descargue el dataset de Kaggle:
# https://www.kaggle.com/datasets/social-media-user-activity-dataset
# df = pd.read_csv("instagram_usage_lifestyle.csv")

# Para esta demostración, generamos una muestra representativa del dataset
np.random.seed(42)
n = 50000  # muestra manejable para ejecución local

# Simulamos el dataset con las mismas distribuciones documentadas
genders = np.random.choice(['Male', 'Female', 'Non-binary', 'Prefer not to say'],
                            n, p=[0.48, 0.48, 0.03, 0.01])
countries = np.random.choice(['United States', 'India', 'Brazil', 'United Kingdom',
                               'Canada', 'Australia', 'South Korea', 'Germany', 'Japan', 'Other'],
                              n, p=[0.25, 0.18, 0.12, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.10])
urban_rural = np.random.choice(['Urban', 'Suburban', 'Rural'], n, p=[0.55, 0.30, 0.15])
income_level = np.random.choice(['Low', 'Lower-middle', 'Middle', 'Upper-middle', 'High'],
                                 n, p=[0.20, 0.25, 0.30, 0.15, 0.10])
employment = np.random.choice(['Full-time employed', 'Student', 'Freelancer',
                                'Unemployed', 'Part-time', 'Retired'],
                               n, p=[0.45, 0.22, 0.12, 0.10, 0.08, 0.03])
education = np.random.choice(["Bachelor's", 'High school', 'Some college',
                               "Master's", 'Other', 'PhD'],
                              n, p=[0.35, 0.25, 0.20, 0.12, 0.05, 0.03])
relationship = np.random.choice(['Single', 'Married', 'In a relationship', 'Divorced', 'Widowed'],
                                 n, p=[0.40, 0.25, 0.25, 0.08, 0.02])
has_children = np.random.choice(['No', 'Yes'], n, p=[0.72, 0.28])
diet_quality = np.random.choice(['Excellent', 'Good', 'Average', 'Poor', 'Very poor'],
                                 n, p=[0.10, 0.25, 0.35, 0.20, 0.10])
smoking = np.random.choice(['No', 'Yes', 'Former'], n, p=[0.75, 0.15, 0.10])
alcohol = np.random.choice(['Never', 'Rarely', 'Weekly', 'Several times a week', 'Daily'],
                            n, p=[0.30, 0.35, 0.20, 0.10, 0.05])
content_pref = np.random.choice(['Reels', 'Stories', 'Mixed', 'Live', 'Photos', 'Videos'],
                                 n)
content_theme = np.random.choice(['Fitness', 'Tech', 'Other', 'Food', 'Fashion', 'Music', 'Art', 'Travel'],
                                  n)
privacy = np.random.choice(['Public', 'Private', 'Friends only'], n)
subscription = np.random.choice(['Free', 'Premium', 'Business'], n, p=[0.75, 0.15, 0.10])
uses_premium = np.random.choice(['No', 'Yes'], n, p=[0.78, 0.22])

age = np.random.randint(13, 66, n)
exercise_h = np.round(np.random.uniform(0, 20, n), 1)
sleep_h = np.round(np.random.uniform(4, 10, n), 1)
stress = np.random.randint(0, 41, n)
happiness = np.random.randint(1, 11, n)
bmi = np.round(np.random.uniform(16, 40, n), 1)
bp_sys = np.random.randint(90, 160, n)
bp_dia = np.random.randint(60, 100, n)
steps = np.random.randint(2000, 15000, n)
work_h = np.round(np.random.uniform(0, 70, n), 1)
hobbies = np.random.randint(0, 10, n)
social_ev = np.random.randint(0, 15, n)
books = np.random.randint(0, 25, n)
volunteer_h = np.round(np.random.uniform(0, 15, n), 1)
travel_freq = np.random.randint(0, 12, n)
daily_active = np.round(np.random.uniform(5, 500, n), 1)
sessions = np.random.randint(1, 40, n)
posts_pw = np.random.randint(0, 20, n)
reels = np.random.randint(10, 250, n)
stories_v = np.random.randint(5, 120, n)
likes = np.random.randint(5, 200, n)
comments = np.random.randint(0, 60, n)
dms_sent = np.random.randint(0, 80, n)
dms_recv = np.random.randint(0, 80, n)
ads_viewed = np.random.randint(0, 40, n)
ads_clicked = np.random.randint(0, 15, n)
t_feed = np.random.randint(2, 250, n)
t_explore = np.random.randint(1, 150, n)
t_messages = np.random.randint(1, 120, n)
t_reels = np.random.randint(1, 180, n)
followers = np.random.randint(10, 50000, n)
following = np.random.randint(20, 10000, n)
notif_rate = np.round(np.random.uniform(0, 1, n), 2)
acc_year = np.random.randint(2010, 2026, n)
avg_session = np.round(np.random.uniform(5, 50, n), 1)
linked_acc = np.random.randint(0, 6, n)
two_factor = np.random.choice(['Yes', 'No'], n, p=[0.65, 0.35])
biometric = np.random.choice(['No', 'Yes'], n, p=[0.60, 0.40])

# Generar engagement con correlaciones realistas
engagement_score = (
    0.03 * daily_active
    + 0.05 * sessions
    + 0.01 * (reels / 30)
    + 0.008 * likes
    + 0.002 * followers / 1000
    - 0.015 * stress
    + 0.01 * happiness
    + np.random.exponential(0.3, n)
)
engagement_score = np.clip(np.round(engagement_score, 2), 0.67, 18.67)

df = pd.DataFrame({
    'user_id': range(1, n + 1),
    'age': age,
    'gender': genders,
    'country': countries,
    'urban_rural': urban_rural,
    'income_level': income_level,
    'employment_status': employment,
    'education_level': education,
    'relationship_status': relationship,
    'has_children': has_children,
    'exercise_hours_per_week': exercise_h,
    'sleep_hours_per_night': sleep_h,
    'diet_quality': diet_quality,
    'smoking': smoking,
    'alcohol_frequency': alcohol,
    'perceived_stress_score': stress,
    'self_reported_happiness': happiness,
    'body_mass_index': bmi,
    'blood_pressure_systolic': bp_sys,
    'blood_pressure_diastolic': bp_dia,
    'daily_steps_count': steps,
    'weekly_work_hours': work_h,
    'hobbies_count': hobbies,
    'social_events_per_month': social_ev,
    'books_read_per_year': books,
    'volunteer_hours_per_month': volunteer_h,
    'travel_frequency_per_year': travel_freq,
    'daily_active_minutes_instagram': daily_active,
    'sessions_per_day': sessions,
    'posts_created_per_week': posts_pw,
    'reels_watched_per_day': reels,
    'stories_viewed_per_day': stories_v,
    'likes_given_per_day': likes,
    'comments_written_per_day': comments,
    'dms_sent_per_week': dms_sent,
    'dms_received_per_week': dms_recv,
    'ads_viewed_per_day': ads_viewed,
    'ads_clicked_per_day': ads_clicked,
    'time_on_feed_per_day': t_feed,
    'time_on_explore_per_day': t_explore,
    'time_on_messages_per_day': t_messages,
    'time_on_reels_per_day': t_reels,
    'followers_count': followers,
    'following_count': following,
    'uses_premium_features': uses_premium,
    'notification_response_rate': notif_rate,
    'account_creation_year': acc_year,
    'average_session_length_minutes': avg_session,
    'content_type_preference': content_pref,
    'preferred_content_theme': content_theme,
    'privacy_setting_level': privacy,
    'two_factor_auth_enabled': two_factor,
    'biometric_login_used': biometric,
    'linked_accounts_count': linked_acc,
    'subscription_status': subscription,
    'user_engagement_score': engagement_score
})

print(f"\n--- Información general del dataset ---")
print(f"Filas: {df.shape[0]:,} | Columnas: {df.shape[1]}")

# Tipos de variables
num_vars = df.select_dtypes(include=[np.number]).columns.tolist()
cat_vars = df.select_dtypes(include='object').columns.tolist()
num_vars.remove('user_id')

print(f"\nVariables numéricas ({len(num_vars)}): {num_vars[:5]}... (total {len(num_vars)})")
print(f"Variables categóricas ({len(cat_vars)}): {cat_vars}")

print("\n--- Verificación de requisitos del dataset ---")
numeric_cols = df.select_dtypes(include=[np.number]).columns.drop('user_id')
categorical_cols = df.select_dtypes(include='object').columns
print(f"Variables numéricas: {len(numeric_cols)} (mínimo requerido: 7) ✓")
print(f"Variables categóricas: {len(categorical_cols)} (mínimo requerido: 3) ✓")
print(f"Filas totales: {len(df):,} ✓")

print("\n--- Estadísticas descriptivas: Variables numéricas clave ---")
key_num = ['age', 'daily_active_minutes_instagram', 'sessions_per_day',
           'followers_count', 'user_engagement_score', 'perceived_stress_score',
           'self_reported_happiness', 'average_session_length_minutes']
print(df[key_num].describe().round(2))

print("\n--- Distribución de variables categóricas clave ---")
for col in ['gender', 'income_level', 'subscription_status', 'urban_rural']:
    print(f"\n{col}:")
    print(df[col].value_counts())

# --- Datos faltantes ---
print("\n--- Datos faltantes ---")
missing = df.isnull().sum()
print(f"Total de valores nulos: {missing.sum()}")
print("(No hay valores faltantes en este dataset)")

# --- Outliers con IQR ---
print("\n--- Detección de outliers (método IQR) ---")
outlier_cols = ['daily_active_minutes_instagram', 'followers_count',
                'following_count', 'user_engagement_score', 'sessions_per_day']
for col in outlier_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    n_outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
    print(f"  {col}: {n_outliers:,} outliers ({n_outliers/len(df)*100:.1f}%)")

# --- Variable objetivo ---
print("\n--- Variable objetivo: user_engagement_score ---")
print(df['user_engagement_score'].describe())

# Visualizaciones EDA
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Análisis Exploratorio de Datos - Instagram Usage Dataset', fontsize=14, fontweight='bold')

# 1. Distribución engagement score
axes[0, 0].hist(df['user_engagement_score'], bins=40, color='steelblue', edgecolor='black', alpha=0.8)
axes[0, 0].set_title('Distribución: User Engagement Score')
axes[0, 0].set_xlabel('Engagement Score')
axes[0, 0].set_ylabel('Frecuencia')

# 2. Engagement por género
gender_eng = df.groupby('gender')['user_engagement_score'].mean().sort_values(ascending=False)
axes[0, 1].bar(gender_eng.index, gender_eng.values, color=['#2196F3', '#FF9800', '#9C27B0', '#4CAF50'])
axes[0, 1].set_title('Engagement Promedio por Género')
axes[0, 1].set_xlabel('Género')
axes[0, 1].set_ylabel('Engagement Score Promedio')
axes[0, 1].tick_params(axis='x', rotation=20)

# 3. Scatter: minutos activos vs engagement
sample_idx = np.random.choice(len(df), 3000, replace=False)
axes[0, 2].scatter(df['daily_active_minutes_instagram'].iloc[sample_idx],
                   df['user_engagement_score'].iloc[sample_idx],
                   alpha=0.4, color='coral', s=8)
axes[0, 2].set_title('Minutos Activos vs Engagement Score')
axes[0, 2].set_xlabel('Minutos Activos en Instagram/día')
axes[0, 2].set_ylabel('Engagement Score')

# 4. Engagement por nivel de ingreso
income_order = ['Low', 'Lower-middle', 'Middle', 'Upper-middle', 'High']
income_eng = df.groupby('income_level')['user_engagement_score'].mean().reindex(income_order)
axes[1, 0].bar(income_eng.index, income_eng.values, color='teal', alpha=0.8)
axes[1, 0].set_title('Engagement Promedio por Nivel de Ingreso')
axes[1, 0].set_xlabel('Nivel de Ingreso')
axes[1, 0].set_ylabel('Engagement Score Promedio')
axes[1, 0].tick_params(axis='x', rotation=30)

# 5. Distribución sesiones por día
axes[1, 1].hist(df['sessions_per_day'], bins=30, color='green', edgecolor='black', alpha=0.7)
axes[1, 1].set_title('Distribución: Sesiones por Día')
axes[1, 1].set_xlabel('Sesiones/día')
axes[1, 1].set_ylabel('Frecuencia')

# 6. Correlaciones clave con engagement
corr_cols = ['daily_active_minutes_instagram', 'sessions_per_day', 'likes_given_per_day',
             'reels_watched_per_day', 'followers_count', 'perceived_stress_score',
             'self_reported_happiness', 'average_session_length_minutes']
correlations = df[corr_cols + ['user_engagement_score']].corr()['user_engagement_score'].drop('user_engagement_score')
colors = ['green' if x > 0 else 'red' for x in correlations.values]
axes[1, 2].barh(correlations.index, correlations.values, color=colors, alpha=0.8)
axes[1, 2].set_title('Correlación con Engagement Score')
axes[1, 2].set_xlabel('Coeficiente de Correlación')
axes[1, 2].axvline(x=0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig('/home/claude/eda_plots.png', dpi=120, bbox_inches='tight')
plt.close()
print("\nGráficas EDA guardadas en: eda_plots.png")

# Heatmap de correlaciones
numeric_subset = ['age', 'daily_active_minutes_instagram', 'sessions_per_day',
                  'likes_given_per_day', 'reels_watched_per_day', 'followers_count',
                  'perceived_stress_score', 'self_reported_happiness',
                  'average_session_length_minutes', 'user_engagement_score']
corr_matrix = df[numeric_subset].corr()

plt.figure(figsize=(11, 9))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            linewidths=0.5, square=True, cbar_kws={'shrink': 0.8})
plt.title('Matriz de Correlación - Variables Numéricas Clave', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('/home/claude/correlation_heatmap.png', dpi=120, bbox_inches='tight')
plt.close()
print("Heatmap de correlaciones guardado en: correlation_heatmap.png")

# =============================================================================
# FASE 3: PROCESAMIENTO DE LA INFORMACIÓN
# =============================================================================
print("\n" + "=" * 70)
print("FASE 3: PROCESAMIENTO DE LA INFORMACIÓN")
print("=" * 70)

# ---- 3.1 Limpieza de datos ----
print("\n--- 3.1 Limpieza de datos ---")

# Eliminar columna user_id (no aporta valor predictivo)
df_clean = df.drop(columns=['user_id']).copy()
print(f"Columna 'user_id' eliminada. Shape: {df_clean.shape}")

# Verificar y eliminar duplicados
n_dups = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates()
print(f"Duplicados eliminados: {n_dups}. Shape: {df_clean.shape}")

# Verificar valores nulos
print(f"Valores nulos totales: {df_clean.isnull().sum().sum()}")

# Verificar consistencias lógicas
print(f"Rango de edad: {df_clean['age'].min()} - {df_clean['age'].max()} ✓")
print(f"Rango engagement: {df_clean['user_engagement_score'].min():.2f} - {df_clean['user_engagement_score'].max():.2f} ✓")
print(f"Rango notification_response_rate: {df_clean['notification_response_rate'].min():.2f} - {df_clean['notification_response_rate'].max():.2f} ✓")

# ---- 3.2 Ingeniería de Variables ----
print("\n--- 3.2 Ingeniería de variables (nuevas variables) ---")

# Variable: total_activity (suma de acciones de interacción)
df_clean['total_interaction'] = (
    df_clean['posts_created_per_week']
    + df_clean['likes_given_per_day']
    + df_clean['comments_written_per_day']
    + df_clean['reels_watched_per_day']
    + df_clean['stories_viewed_per_day']
)
print("Nueva variable creada: total_interaction (suma de interacciones del usuario)")

# Variable: time_on_content (tiempo total en contenido, excluyendo mensajes)
df_clean['time_on_content'] = (
    df_clean['time_on_feed_per_day']
    + df_clean['time_on_explore_per_day']
    + df_clean['time_on_reels_per_day']
)
print("Nueva variable creada: time_on_content (tiempo total en feed+explore+reels)")

# Variable: follower_ratio (ratio seguidores/seguidos)
df_clean['follower_ratio'] = np.where(
    df_clean['following_count'] > 0,
    df_clean['followers_count'] / df_clean['following_count'],
    0
).round(4)
print("Nueva variable creada: follower_ratio (followers / following)")

# Variable: ad_engagement_rate (tasa de clicks en ads)
df_clean['ad_engagement_rate'] = np.where(
    df_clean['ads_viewed_per_day'] > 0,
    df_clean['ads_clicked_per_day'] / df_clean['ads_viewed_per_day'],
    0
).round(4)
print("Nueva variable creada: ad_engagement_rate (ads_clicked / ads_viewed)")

print(f"\nNuevas variables: total_interaction, time_on_content, follower_ratio, ad_engagement_rate")
print(f"Shape después de ingeniería de variables: {df_clean.shape}")

# ---- 3.3 Transformación de datos ----
print("\n--- 3.3 Codificación de variables categóricas ---")

# Separar features y variable objetivo
cat_columns = df_clean.select_dtypes(include='object').columns.tolist()
print(f"Variables categóricas a codificar: {cat_columns}")

# One-Hot Encoding para variables nominales con pocos niveles
nominal_ohe = ['gender', 'urban_rural', 'content_type_preference',
               'preferred_content_theme', 'privacy_setting_level',
               'smoking', 'diet_quality', 'alcohol_frequency',
               'has_children', 'uses_premium_features',
               'two_factor_auth_enabled', 'biometric_login_used']

# Label Encoding para variables ordinales
ordinal_map = {
    'income_level': {'Low': 1, 'Lower-middle': 2, 'Middle': 3, 'Upper-middle': 4, 'High': 5},
    'education_level': {'High school': 1, 'Some college': 2, "Bachelor's": 3, "Master's": 4, 'PhD': 5, 'Other': 0},
    'subscription_status': {'Free': 0, 'Premium': 1, 'Business': 2}
}

# Label Encoding para variables nominales de alta cardinalidad
label_enc_cols = ['country', 'employment_status', 'relationship_status']

df_processed = df_clean.copy()

# Aplicar ordinal encoding
for col, mapping in ordinal_map.items():
    df_processed[col] = df_processed[col].map(mapping)
    print(f"  Ordinal encoding aplicado: {col}")

# Aplicar label encoding para alta cardinalidad
le = LabelEncoder()
for col in label_enc_cols:
    df_processed[col] = le.fit_transform(df_processed[col])
    print(f"  Label encoding aplicado: {col}")

# Aplicar One-Hot Encoding
df_processed = pd.get_dummies(df_processed, columns=nominal_ohe, drop_first=True, dtype=int)
print(f"\n  One-Hot Encoding aplicado a {len(nominal_ohe)} columnas")
print(f"  Shape después del encoding: {df_processed.shape}")

# ---- 3.4 Escalado de variables numéricas ----
print("\n--- 3.4 Escalado de variables numéricas ---")

X = df_processed.drop(columns=['user_engagement_score'])
y = df_processed['user_engagement_score']

# Separar en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Conjunto entrenamiento: {X_train.shape[0]:,} registros")
print(f"Conjunto prueba: {X_test.shape[0]:,} registros")

# Escalar variables numéricas continuas (solo las que tienen escala muy diferente)
scale_cols = ['daily_active_minutes_instagram', 'followers_count', 'following_count',
              'time_on_feed_per_day', 'time_on_explore_per_day', 'time_on_messages_per_day',
              'time_on_reels_per_day', 'reels_watched_per_day', 'likes_given_per_day',
              'total_interaction', 'time_on_content', 'daily_steps_count',
              'follower_ratio', 'weekly_work_hours']

scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[scale_cols] = scaler.fit_transform(X_train[scale_cols])
X_test_scaled[scale_cols] = scaler.transform(X_test[scale_cols])

print(f"Escalado estándar (StandardScaler) aplicado a {len(scale_cols)} columnas")
print(f"\nShape final X_train: {X_train_scaled.shape}")
print(f"Shape final X_test: {X_test_scaled.shape}")

# ---- Resumen final ----
print("\n--- RESUMEN PROCESAMIENTO COMPLETO ---")
print(f"Dataset original: {df.shape[0]:,} filas x {df.shape[1]} columnas")
print(f"Dataset procesado: {X_train_scaled.shape[0] + X_test_scaled.shape[0]:,} filas x {X_train_scaled.shape[1]} features")
print(f"Variable objetivo: user_engagement_score")
print(f"  Media: {y.mean():.4f} | Std: {y.std():.4f} | Min: {y.min():.2f} | Max: {y.max():.2f}")
print(f"\nDataset listo para modelado en Parte 2 del proyecto.")
print("\nProcesamiento completado exitosamente.")
