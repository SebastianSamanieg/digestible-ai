# Introducción a la Inteligencia Artificial

> 📽️ **Recurso recomendado:** Ver la película *El Código Enigma (The Imitation Game, 2014)* — narra la historia de Alan Turing, pionero de la computación y padre conceptual de la IA.

---

## 1. Evolución Histórica de la IA ("Capas de la Cebolla")

La inteligencia artificial no surgió de un momento a otro; evolucionó en capas progresivas:

| Capa | Campo | Década de auge |
|------|-------|----------------|
| 1 | Inteligencia Artificial (IA) | 1960s |
| 2 | Machine Learning (ML) | 1980s |
| 3 | Deep Learning (DL) | 2010s |
| 4 | IA Generativa | 2020s |
| 5 | IA Agéntica | 2024+ |

> **Nota histórica:** El primer **perceptrón** (neurona artificial) fue creado en los años 50. Hubo un período conocido como el **"Invierno de la IA"** causado por las limitaciones tecnológicas de la época. Las redes neuronales profundas solo se volvieron viables con la llegada de las **GPUs (tarjetas gráficas)**, que permitieron el procesamiento paralelo masivo necesario para entrenarlas.

---

## 2. ¿Qué es la Inteligencia Artificial?

La **IA** busca imitar comportamientos y capacidades cognitivas humanas mediante algoritmos y modelos computacionales.

---

## 3. Machine Learning (ML)

El **Machine Learning** es una rama de la IA que consiste en crear algoritmos que **aprenden patrones a partir de datos**, sin ser programados explícitamente para cada tarea.

### 3.1 Tipos de datos de entrada

- **Datos estructurados:** tablas, bases de datos, hojas de cálculo → se trabajan con algoritmos clásicos de ML.
- **Datos no estructurados:** imágenes, video, audio, texto → requieren **Deep Learning**.

### 3.2 Tipos de Aprendizaje

#### Aprendizaje Supervisado
El modelo aprende a partir de datos **etiquetados** (con respuesta correcta conocida). La variable que queremos predecir se llama **variable objetivo**.

| Tipo de variable objetivo | Tipo de tarea | Ejemplo |
|---------------------------|---------------|---------|
| Continua (números reales) | **Regresión** | Predecir el precio de una casa |
| Discreta (categorías) | **Clasificación** | Detectar si un correo es spam o no |

> En este curso nos enfocaremos principalmente en **algoritmos supervisados**.

#### Aprendizaje No Supervisado
El modelo trabaja con datos **sin etiquetas**; encuentra patrones y estructuras por sí solo.

- **Clustering (Segmentación / Clusterización):** agrupa datos similares en grupos llamados *clusters*. Ejemplo: segmentar clientes por comportamiento de compra.

#### Aprendizaje por Refuerzo (*Reinforcement Learning*)
El modelo aprende por **prueba y error**, recibiendo recompensas o penalizaciones según sus acciones. Requiere definir una **función de recompensa** como referencia.

- Algoritmo representativo: **Q-Learning**
- Aplicaciones: juegos, robótica, sistemas de recomendación.

---

## 4. Deep Learning y Redes Neuronales

Cuando los datos son **no estructurados**, los algoritmos clásicos de ML tienen limitaciones. Las **redes neuronales artificiales** (inspiradas en el cerebro humano) son capaces de aprender representaciones complejas directamente de estos datos.

- A medida que aumenta la complejidad del modelo, **aumenta el costo computacional** (se requieren más recursos de hardware).

### Procesamiento de Lenguaje Natural (NLP)
Subcampo del Deep Learning aplicado a **textos**. Permite a las máquinas entender, generar y traducir lenguaje humano.

### ¿Qué es un Token?
Un **token** es la unidad mínima de texto que procesa un modelo de lenguaje. Puede ser una palabra completa, una parte de una palabra, o un signo de puntuación.

- Ejemplo: la frase `"inteligencia artificial"` puede tokenizarse como `["inteligencia", "artifi", "cial"]` dependiendo del tokenizador.
- Los modelos de lenguaje cobran y miden su capacidad en tokens.

### ¿Qué son los Embeddings?
Los **embeddings** son representaciones vectoriales (numéricas) de palabras u otros elementos de texto dentro de un espacio multidimensional.

- Permiten que el modelo "entienda" semánticamente las palabras: palabras con significados similares tienen vectores cercanos.
- Se construyen a partir de un **corpus** (conjunto grande de texto).
- Ejemplo: el vector de "rey" − "hombre" + "mujer" ≈ vector de "reina".

---

## 5. Forecasting (Pronóstico)

El **forecasting** es la predicción de valores futuros a partir de datos históricos. Es un caso especial de regresión aplicado a **series de tiempo**.

- Ejemplos: predecir ventas del próximo mes, demanda de energía, precio de acciones.

---

## 6. Metodología CRISP-DM

**CRISP-DM** (*Cross Industry Standard Process for Data Mining*) es el estándar metodológico para el desarrollo de proyectos de Machine Learning y ciencia de datos. Define un proceso iterativo de 6 fases:

```
1. Comprensión del negocio  →  Definir el objetivo y el ROI esperado
2. Comprensión de los datos →  Explorar y recopilar datos relevantes
3. Preparación de los datos →  Limpieza, transformación, feature engineering
4. Modelado               →  Selección y entrenamiento de algoritmos
5. Evaluación             →  Medir el desempeño y validar contra el objetivo
6. Despliegue             →  Poner el modelo en producción
```

> El diagrama de CRISP-DM es **cíclico**: los resultados de etapas posteriores pueden llevar a regresar a etapas anteriores. Su objetivo es maximizar el **ROI (Retorno sobre la Inversión)** del proyecto.

---

## 7. Ingeniería de Prompts

La **Ingeniería de Prompts** es la práctica de diseñar instrucciones efectivas para interactuar con modelos de lenguaje (LLMs). Una estructura recomendada es:

| Componente | Descripción |
|------------|-------------|
| **Rol** | Indica al modelo qué personaje o experto debe asumir |
| **Contexto** | Proporciona información de fondo relevante |
| **Tarea** | Describe claramente lo que se quiere obtener |
| **Formato esperado** | Especifica cómo debe presentarse la respuesta (tabla, lista, párrafo, etc.) |
| **Restricciones o criterios** | Define límites, tono, longitud u otras condiciones |

---

## 8. Fundamentos Estadísticos para ML

> Para aplicar Machine Learning correctamente se requieren **nociones de estadística y probabilidad**.

### 8.1 Conceptos Clave

| Término | Definición |
|---------|------------|
| **Dato** | Observación individual (un valor registrado) |
| **Parámetro** | Valor que describe una característica de la **población** (generalmente desconocido) |
| **Estadístico** | Valor calculado a partir de una **muestra** para estimar un parámetro |
| **Población** | Conjunto completo de elementos con una característica en común |
| **Muestra** | Subconjunto representativo de la población |
| **Homogeneidad** | Baja variabilidad entre los elementos de un conjunto |
| **Heterogeneidad** | Alta variabilidad entre los elementos de un conjunto |

---

### 8.2 Tipos de Variables

#### Variables Cualitativas (Categóricas)
| Subtipo | Descripción | Ejemplo |
|---------|-------------|---------|
| **Nominal** | Sin orden entre categorías | Color, género, país |
| **Ordinal** | Con orden natural entre categorías | Nivel educativo, escala de satisfacción |

#### Variables Cuantitativas (Numéricas)
| Subtipo | Descripción | Ejemplo |
|---------|-------------|---------|
| **Discreta** | Valores enteros contables | Número de hijos, cantidad de ventas |
| **Continua** | Cualquier valor en un rango | Temperatura, peso, ingresos |

---

### 8.3 Estadística Descriptiva

La estadística descriptiva resume y organiza la información de un conjunto de datos.

#### Análisis Univariado (una sola variable)

**Para variables cualitativas:**
- Tabla de frecuencias (absolutas y relativas)
- Diagrama de barras
- Diagrama de sectores (gráfico de torta / pie chart)

**Para variables cuantitativas:**
- Tabla de frecuencias agrupadas
- Histograma
- Polígono de frecuencias
- Diagrama de caja y bigote (*Box Plot*)
- **Medidas de tendencia central:** media, mediana, moda
- **Medidas de dispersión:** varianza, desviación estándar, rango
- **Medidas de localización:** percentiles, cuartiles

---

### 8.4 Análisis Bivariado (dos variables)

Estudia la relación entre dos variables.

- **Coeficiente de correlación de Pearson (r):** mide la fuerza y dirección de la relación lineal entre dos variables cuantitativas. Toma valores entre −1 y +1.
  - `r ≈ +1`: correlación positiva fuerte
  - `r ≈ −1`: correlación negativa fuerte
  - `r ≈ 0`: sin correlación lineal

- **Matriz de correlación:** tabla que muestra los coeficientes de Pearson entre todas las pares de variables de un dataset. Es fundamental en la etapa de exploración de datos (EDA) antes de construir un modelo.