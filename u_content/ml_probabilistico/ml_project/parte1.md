# Proyecto Grupal Final – Parte 1
## Machine Learning Probabilístico
### Predicción del Potencial Publicitario de Usuarios en Instagram

---

## Fase 1: Entendimiento del Negocio

### Descripción del Problema

En el ecosistema del marketing digital, Instagram representa una de las plataformas publicitarias más importantes del mundo. Sin embargo, no todos los usuarios tienen el mismo valor para los anunciantes: algunos pasan horas navegando e interactuando activamente con el contenido, mientras que otros tienen una presencia mínima y pasiva. Esta diferencia impacta directamente en la efectividad y el retorno de inversión de las campañas publicitarias.

El problema que este proyecto busca resolver es la **falta de un modelo predictivo que permita estimar el potencial publicitario de un usuario de Instagram**, entendido como la combinación de su tiempo de exposición a anuncios y su probabilidad de interactuar con ellos. Actualmente, las decisiones de segmentación publicitaria se basan en reglas estáticas o métricas históricas simples, sin aprovechar el poder predictivo de variables demográficas, de comportamiento y de bienestar del usuario.

### Objetivo General

Desarrollar un sistema de predicción en dos etapas que estime, primero, el tiempo diario activo de un usuario en Instagram y, segundo, clasifique a dicho usuario en un segmento de valor publicitario (Alto, Medio o Bajo), con el fin de apoyar la toma de decisiones en estrategias de marketing digital.

### Objetivos Específicos

1. Construir un modelo de regresión que prediga los minutos diarios activos de un usuario en Instagram (`daily_active_minutes_instagram`) a partir de sus características demográficas, de comportamiento y de salud.
2. Desarrollar un modelo de clasificación que categorice a los usuarios en segmentos de valor publicitario (Alto, Medio, Bajo) utilizando variables de engagement y comportamiento en la plataforma.
3. Identificar las variables más influyentes en la determinación del potencial publicitario de un usuario, con el fin de generar insights accionables para equipos de marketing.

### Stakeholders

| Stakeholder | Rol | Interés |
|---|---|---|
| Agencias de publicidad digital | Usuario principal del modelo | Optimizar la inversión publicitaria segmentando audiencias de alto valor |
| Marcas anunciantes en Instagram | Beneficiario directo | Aumentar el ROI de sus campañas al dirigirse a usuarios con mayor probabilidad de interacción |
| Equipo de ciencia de datos | Desarrollador | Construir y mantener modelos precisos y reproducibles |
| Usuarios de Instagram | Afectado indirecto | Recibir publicidad más relevante y menos intrusiva |

### Restricciones

- El dataset utilizado corresponde exclusivamente a usuarios de Instagram, por lo que los modelos no son generalizables a otras plataformas sin reentrenamiento.
- Las predicciones se basan en patrones históricos de comportamiento y no consideran eventos externos (cambios de algoritmo, tendencias virales, etc.).
- El modelo no recolecta datos en tiempo real; opera sobre snapshots del comportamiento del usuario.
- Se deben respetar principios de privacidad y uso ético de los datos, evitando la discriminación por variables sensibles como género, religión o condición de salud.

### Definición de Éxito

El proyecto se considerará exitoso si se cumplen los siguientes criterios:

**Modelo de Regresión (Etapa 1):**
- Coeficiente de determinación R² ≥ 0.70
- Error Cuadrático Medio (RMSE) dentro de un rango aceptable respecto a la escala de la variable objetivo

**Modelo de Clasificación (Etapa 2):**
- Exactitud (Accuracy) ≥ 75%
- F1-Score macro ≥ 0.70, garantizando buen desempeño en todas las clases

---

## Fase 2: Entendimiento de los Datos

### Descripción del Dataset

- **Fuente:** Kaggle – [Social Media User Activity Dataset](https://www.kaggle.com/datasets/sadiajavedd/social-media-user-activity-dataset)
- **Plataforma cubierta:** Instagram
- **Número de registros:** 1,547,896 filas
- **Número de variables:** 58 columnas
- **Tamaño en memoria:** ~874.2 MB

El dataset contiene información detallada sobre el perfil demográfico, hábitos de vida, comportamiento dentro de Instagram y métricas de engagement de más de un millón y medio de usuarios. Cada fila representa un usuario único con sus respectivos atributos.

### Tipos de Variables

**Variables numéricas (float64 / int64) — 38 variables:**

| Variable | Tipo | Descripción |
|---|---|---|
| `age` | int64 | Edad del usuario |
| `exercise_hours_per_week` | float64 | Horas de ejercicio por semana |
| `sleep_hours_per_night` | float64 | Horas de sueño por noche |
| `perceived_stress_score` | int64 | Puntuación de estrés percibido (escala numérica) |
| `self_reported_happiness` | int64 | Felicidad autoreportada (escala numérica) |
| `body_mass_index` | float64 | Índice de masa corporal |
| `blood_pressure_systolic` | int64 | Presión arterial sistólica |
| `blood_pressure_diastolic` | int64 | Presión arterial diastólica |
| `daily_steps_count` | int64 | Pasos diarios |
| `weekly_work_hours` | float64 | Horas de trabajo semanales |
| `hobbies_count` | int64 | Número de hobbies |
| `social_events_per_month` | int64 | Eventos sociales por mes |
| `books_read_per_year` | int64 | Libros leídos al año |
| `volunteer_hours_per_month` | float64 | Horas de voluntariado al mes |
| `travel_frequency_per_year` | int64 | Frecuencia de viajes al año |
| `daily_active_minutes_instagram` | float64 | **Variable objetivo Etapa 1** – Minutos diarios activos en Instagram |
| `sessions_per_day` | int64 | Sesiones por día en la app |
| `posts_created_per_week` | int64 | Posts creados por semana |
| `reels_watched_per_day` | int64 | Reels vistos por día |
| `stories_viewed_per_day` | int64 | Stories vistas por día |
| `likes_given_per_day` | int64 | Likes dados por día |
| `comments_written_per_day` | int64 | Comentarios escritos por día |
| `dms_sent_per_week` | int64 | DMs enviados por semana |
| `dms_received_per_week` | int64 | DMs recibidos por semana |
| `ads_viewed_per_day` | int64 | Anuncios vistos por día |
| `ads_clicked_per_day` | int64 | Anuncios clickeados por día |
| `time_on_feed_per_day` | int64 | Tiempo en feed por día (min) |
| `time_on_explore_per_day` | int64 | Tiempo en explorar por día (min) |
| `time_on_messages_per_day` | int64 | Tiempo en mensajes por día (min) |
| `time_on_reels_per_day` | int64 | Tiempo en reels por día (min) |
| `followers_count` | int64 | Número de seguidores |
| `following_count` | int64 | Número de seguidos |
| `notification_response_rate` | float64 | Tasa de respuesta a notificaciones |
| `account_creation_year` | int64 | Año de creación de la cuenta |
| `average_session_length_minutes` | float64 | Duración promedio de sesión (min) |
| `linked_accounts_count` | int64 | Número de cuentas vinculadas |
| `user_engagement_score` | float64 | **Insumo para variable objetivo Etapa 2** – Score de engagement |

**Variables categóricas (str) — 20 variables:**

| Variable | Descripción |
|---|---|
| `app_name` | Nombre de la red social (Instagram) |
| `gender` | Género del usuario |
| `country` | País de residencia |
| `urban_rural` | Entorno urbano o rural |
| `income_level` | Nivel de ingresos |
| `employment_status` | Estado laboral |
| `education_level` | Nivel educativo |
| `relationship_status` | Estado civil/relación |
| `has_children` | Tiene hijos (Sí/No) |
| `diet_quality` | Calidad de dieta |
| `smoking` | Fuma (Sí/No) |
| `alcohol_frequency` | Frecuencia de consumo de alcohol |
| `uses_premium_features` | Usa funciones premium (Sí/No) |
| `last_login_date` | Fecha del último login |
| `content_type_preference` | Preferencia de tipo de contenido |
| `preferred_content_theme` | Temática de contenido preferida |
| `privacy_setting_level` | Nivel de privacidad de la cuenta |
| `two_factor_auth_enabled` | Autenticación de dos factores (Sí/No) |
| `biometric_login_used` | Usa login biométrico (Sí/No) |
| `subscription_status` | Estado de suscripción (Free/Premium) |

### Variables Objetivo y Predictoras

#### Etapa 1 — Modelo de Regresión

| Rol | Variable | Justificación |
|---|---|---|
| **Variable objetivo** | `daily_active_minutes_instagram` | Representa el tiempo total de exposición del usuario en la plataforma |
| **Predictoras principales** | `sessions_per_day`, `average_session_length_minutes`, `reels_watched_per_day`, `stories_viewed_per_day`, `time_on_feed_per_day`, `time_on_reels_per_day` | Comportamiento directo dentro de la app |
| **Predictoras secundarias** | `age`, `employment_status`, `weekly_work_hours`, `sleep_hours_per_night`, `self_reported_happiness` | Factores de estilo de vida que condicionan el tiempo disponible |

#### Etapa 2 — Modelo de Clasificación

| Rol | Variable | Justificación |
|---|---|---|
| **Variable objetivo** | `segmento_publicitario` *(variable derivada)* | Clasificación en Alto/Medio/Bajo basada en `user_engagement_score` + `ads_clicked_per_day` |
| **Predictoras principales** | `daily_active_minutes_instagram` *(output Etapa 1)*, `ads_viewed_per_day`, `ads_clicked_per_day`, `notification_response_rate`, `likes_given_per_day`, `comments_written_per_day` | Indicadores directos de interacción con contenido y publicidad |
| **Predictoras secundarias** | `income_level`, `age`, `content_type_preference`, `preferred_content_theme`, `followers_count` | Variables de perfil que modulan el tipo de interacción |

### Análisis Exploratorio Preliminar

**Datos faltantes:** El dataset no presenta valores nulos en ninguna de sus 58 columnas (1,547,896 non-null en todas). Esto elimina la necesidad de estrategias de imputación, aunque se verificará en la fase de procesamiento.

**Observaciones sobre distribuciones (basado en muestra):**
- `age` varía entre usuarios jóvenes y adultos mayores, con presencia de múltiples grupos etarios.
- `perceived_stress_score` y `self_reported_happiness` presentan valores en extremos opuestos en algunos registros, lo que sugiere distribuciones amplias.
- `daily_active_minutes_instagram` tiene alta variabilidad (desde 5 min hasta más de 230 min en la muestra), lo que la hace una variable objetivo rica para regresión.
- `sessions_per_day` varía entre 1 y 14+ en la muestra, indicando perfiles de uso muy distintos.

**Problemas identificados:**
- `last_login_date` está en formato string y deberá convertirse a tipo fecha para extraer variables útiles (días desde último login, mes, etc.).
- `account_creation_year` podría transformarse en **antigüedad de cuenta** para mayor poder predictivo.
- La variable objetivo de clasificación (`segmento_publicitario`) debe **crearse** a partir de la combinación de `user_engagement_score` y `ads_clicked_per_day`, requiriendo una decisión de umbralización.
- Variables como `app_name` y `subscription_status` tienen baja variabilidad en la muestra y podrían ser poco informativas.

### Cumplimiento de Requisitos del Dataset

| Requisito | Valor requerido | Valor del dataset |
|---|---|---|
| Variables numéricas | ≥ 7 | 38 ✅ |
| Variables categóricas | ≥ 3 | 20 ✅ |
| Número de filas | Suficiente para ML | 1,547,896 ✅ |

---

## Fase 3: Procesamiento de la Información

> ⚠️ *Esta fase se desarrolla en detalle en el código fuente adjunto (Python). A continuación se documenta el proceso seguido.*

### 3.1 Limpieza de Datos

**Valores faltantes:** El dataset no presenta valores nulos. Se verificó con `df.isnull().sum()` confirmando 0 nulos en todas las columnas.

**Duplicados:** Se verificará la existencia de filas duplicadas con `df.duplicated().sum()` y se eliminarán en caso de encontrarse.

**Inconsistencias identificadas y tratamiento:**
- `last_login_date`: convertida de string a datetime con `pd.to_datetime()`.
- Valores extremos en variables de comportamiento (ej. `reels_watched_per_day` = 241 en muestra): se analizarán con IQR para determinar si son outliers legítimos o errores de captura.

### 3.2 Transformación de Datos

**Ingeniería de variables:**

| Variable nueva | Origen | Descripción |
|---|---|---|
| `account_age_years` | `account_creation_year` | Antigüedad de la cuenta en años (2025 - año creación) |
| `days_since_last_login` | `last_login_date` | Días transcurridos desde el último login |
| `ad_interaction_rate` | `ads_clicked_per_day / ads_viewed_per_day` | Tasa de interacción con publicidad |
| `segmento_publicitario` | `user_engagement_score` + `ads_clicked_per_day` | Variable objetivo Etapa 2: Alto / Medio / Bajo |

**Codificación de variables categóricas:**
- Variables binarias (`smoking`, `has_children`, `uses_premium_features`, etc.): codificación Label Encoding (0/1).
- Variables ordinales (`income_level`, `diet_quality`, `education_level`): codificación ordinal respetando el orden natural.
- Variables nominales (`gender`, `country`, `content_type_preference`, etc.): codificación One-Hot Encoding.

**Normalización / Escalado:**
- Para el modelo de regresión se aplicará **StandardScaler** a las variables numéricas con alta varianza.
- Para el modelo de clasificación se evaluará el uso de **MinMaxScaler** según el algoritmo seleccionado.

### 3.3 Construcción de la Variable Objetivo de Clasificación

La variable `segmento_publicitario` se construirá mediante la siguiente lógica:

```
Puntaje_publicitario = (user_engagement_score × 0.6) + (ad_interaction_rate × 0.4)

Alto  → Percentil 66–100
Medio → Percentil 33–65
Bajo  → Percentil 0–32
```

Los pesos y umbrales exactos se ajustarán tras el análisis de la distribución completa del dataset.

### 3.4 División del Dataset

Dado el tamaño del dataset (1.5M+ registros), se realizará una **muestra estratificada** para el desarrollo y validación inicial de los modelos:

- **Muestra de trabajo:** 10% del total (~154,000 registros), manteniendo proporciones de las variables categóricas clave.
- **División train/test:** 80% entrenamiento / 20% prueba.
- **Validación:** K-Fold Cross Validation (k=5) para garantizar robustez.

---

*Documento elaborado como parte del proyecto grupal de Machine Learning Probabilístico — Entrega Parte 1.*