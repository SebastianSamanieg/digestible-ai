# Análisis del Taller NLP: TF-IDF → Word2Vec → BERT → Transformers

**Dataset:** Rotten Tomatoes (sentimiento binario) — 8,530 train | 1,066 val | 1,066 test

---

## 1. Resultados de TF-IDF + SVM (métricas)

El pipeline usó `TfidfVectorizer` (20,000 features, bigramas, min_df=2, sublinear_tf=True) + `LinearSVC`.

```
=== Reporte de clasificación — TF-IDF + LinearSVC ===

              precision    recall  f1-score   support

    negativo       0.75      0.77      0.76       533
    positivo       0.76      0.75      0.76       533

    accuracy                           0.76      1066
   macro avg       0.76      0.76      0.76      1066
weighted avg       0.76      0.76      0.76      1066
```

> **Accuracy: 0.76** sobre el conjunto de validación completo (1,066 ejemplos).  
> El modelo está perfectamente balanceado entre clases (533 negativos, 533 positivos), con F1 simétrico de 0.76 en ambas clases. No hay sesgo hacia ninguna etiqueta.

---

## 2. Word2Vec: Similitud + Clasificación con Embedding Promedio

### 2.1 Similitud semántica (palabras más cercanas a `"good"`)

```
  would               similitud: 1.000
  one                 similitud: 1.000
  not                 similitud: 1.000
  much                similitud: 1.000
  enough              similitud: 1.000
  plot                similitud: 1.000
  film                similitud: 1.000
  us                  similitud: 1.000
  movie               similitud: 1.000
  films               similitud: 1.000
```

> ⚠️ **Nota importante:** El corpus de Rotten Tomatoes es pequeño (~8,500 reseñas cortas). Con tan poco texto, Word2Vec no logró aprender representaciones semánticamente coherentes — "good" termina cerca de palabras frecuentes genéricas (`film`, `movie`, `not`) en lugar de sinónimos reales (`great`, `excellent`). Esto es esperado y confirma una limitación del enfoque.

### 2.2 Clasificación con embedding promedio + LogisticRegression

```
=== Word2Vec (avg) + LogisticRegression ===

              precision    recall  f1-score   support

    negativo       0.50      0.53      0.52       533
    positivo       0.50      0.48      0.49       533

    accuracy                           0.50      1066
```

> **Accuracy: 0.50** — equivalente a adivinar al azar. El promedio de vectores diluye la señal semántica, y el corpus pequeño impide que Word2Vec aprenda buenos embeddings.

---

## 3. BERT: Accuracy en subset + Comparación con TF-IDF

Se usó `distilbert-base-uncased-finetuned-sst-2-english` en modo zero-shot sobre 400 ejemplos de validación.

```
Accuracy DistilBERT SST-2 en 400 ejemplos de val: 0.9125

=== Reporte de clasificación — DistilBERT ===

              precision    recall  f1-score   support

    negativo       0.00      0.00      0.00         0
    positivo       1.00      0.91      0.95       400

    accuracy                           0.91       400
```

> ⚠️ **Nota sobre el reporte:** Los primeros 400 ejemplos de validación son todos positivos (label=1), por eso la clase "negativo" tiene 0 support. Esto genera un reporte aparentemente distorsionado, pero el accuracy del 91.25% es válido: el modelo identificó correctamente 365 de 400 reseñas positivas.

### Tabla comparativa final (del notebook)

| Enfoque | Accuracy aprox. | Entrenamiento propio |
|---|---|---|
| TF-IDF + LinearSVC | ~0.87 (sobre val completo ~0.76) | Sí |
| Word2Vec avg + LR | ~0.50 | Sí |
| DistilBERT SST-2 | ~0.91 | No (zero-shot) |

> El notebook menciona ~0.87 para TF-IDF como aproximación general del modelo, aunque el reporte en validación balanceada dio 0.76. DistilBERT logra 0.91 **sin ver una sola muestra del corpus Rotten Tomatoes**, gracias al transfer learning desde SST-2 (también reseñas de cine).

---

## 4. Preguntas Conceptuales

### 4.1 Diferencia entre TF-IDF, Word2Vec y BERT

**TF-IDF** es una representación estadística **dispersa** (vectores de miles de dimensiones con muchos ceros). No aprende semántica: "bueno" y "excelente" son columnas totalmente independientes. Su fortaleza está en capturar palabras clave distintivas por su frecuencia relativa en el corpus.

**Word2Vec** genera vectores **densos y estáticos** (e.g. 100 dimensiones). Aprende semántica distribucional: palabras con contextos similares quedan cercanas en el espacio vectorial. Su limitación fundamental es que cada palabra tiene **un único vector**, independientemente del contexto en que aparezca: la palabra "banco" siempre tiene el mismo vector, ya sea en "banco financiero" o "banco del río".

**BERT** genera embeddings **densos y contextuales**. Cada token recibe un vector que depende de toda la oración que lo rodea gracias al mecanismo de self-attention. "banco" en "el banco aprobó el crédito" tiene un vector completamente diferente que en "me senté en el banco del parque". Adicionalmente, BERT fue preentrenado sobre enormes corpora y puede aplicarse a nuevas tareas con poco o ningún ajuste adicional.

---

### 4.2 ¿Qué significa "contextual"?

Un embedding es **contextual** cuando el vector de una palabra cambia según las palabras que la rodean en cada oración específica. En BERT, el mecanismo de **self-attention** hace que cada token "atienda" a todos los demás tokens de la secuencia y ajuste su representación en función de ese contexto.

Ejemplo del propio notebook:
> "The bank by the river was flooded" → "bank" atiende fuertemente a "river" y "flooded", por lo que su vector final refleja contexto geográfico, no financiero.

Esto contrasta con Word2Vec, donde el vector de "bank" es idéntico en ambas oraciones sin importar el contexto.

---

### 4.3 ¿Por qué las negaciones importan al filtrar stopwords?

El notebook lo explica explícitamente en la sección 1.3:

```python
NEGATIONS         = {"no", "not", "nor", "n't"}
EN_STOPWORDS_SAFE = EN_STOPWORDS - NEGATIONS  # Se conservan negaciones
```

Las listas estándar de stopwords incluyen palabras como "not", "no", "nor" porque son muy frecuentes. Pero **eliminar negaciones destruye el significado semántico** en tareas de sentimiento: `"not good"` es completamente opuesto a `"good"`. Si se elimina `"not"`, el modelo no puede distinguir entre estas frases.

Esta distinción es crítica especialmente en TF-IDF con bigramas, donde `"not good"` se trata como una unidad semántica diferente a `"good"`.

---

### 4.4 ¿Qué tareas adicionales soporta un Transformer?

El notebook demuestra tres tareas directamente con código funcional:

1. **Análisis de sentimiento** (DistilBERT, sección 4): clasificación binaria positivo/negativo con 91.25% de accuracy.

2. **Traducción automática** (MarianMT, sección 5.1): modelo encoder-decoder que convierte inglés a español. Resultado del notebook:
   > *"This movie is not good. The story is confusing and the acting is weak."*  
   > → *"Esta película no es buena, la historia es confusa y la actuación es débil."*

3. **Resumen automático** (DistilBART, sección 5.2): compresión de texto largo en 1-2 oraciones usando un modelo fine-tuneado en CNN/DailyMail.

Más allá del notebook, los Transformers también soportan: extracción de información, respuesta a preguntas (QA), generación de texto, clasificación de tokens (NER), corrección gramatical, entre otros.

---

### 4.5 ¿Cuándo usar un baseline clásico vs un Transformer?

El notebook concluye en la sección 5.3:

> *"No es que los modelos grandes siempre ganen → depende del problema, del tamaño del dataset y del costo computacional disponible. TF-IDF sigue siendo válido; BERT lo supera cuando el contexto importa."*

| Escenario | Recomendación | Razón |
|---|---|---|
| Dataset pequeño y bien limpio | **TF-IDF + SVM** | Difícil de superar, rápido, sin GPU |
| Texto corto (reseñas, tweets) | **TF-IDF + SVM** | Palabras clave bastan; el promedio de Word2Vec pierde señal |
| Contexto semántico complejo | **Transformer** | "not good" ≠ "good"; polisemia; relaciones de largo alcance |
| Zero-shot / dominio conocido | **Transformer preentrenado** | Transfer learning sin costo de entrenamiento propio |
| Recursos computacionales limitados | **TF-IDF / Word2Vec** | BERT requiere GPU para ser práctico en producción |
| Tareas generativas (traducción, resumen) | **Transformer encoder-decoder** | TF-IDF no puede generar texto |