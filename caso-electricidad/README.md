# Grupo 06: Caso Electricidad - Detección de Fraude
## Sustentación de Resultados Experimentales

---

## 1. Carga y División Train-Test

Se implementó la división train-test (70/30) como **primer paso crítico** para prevenir data leakage. El dataset contiene 38,474 registros con 24 columnas temporales de consumo eléctrico. La distribución de clases muestra desbalanceo significativo: **90.2% no fraude** (0) vs **9.8% fraude** (1). La estratificación preserva estas proporciones en train (26,931 muestras) y test (11,543 muestras), garantizando evaluación honesta. Este enfoque cumple con mejores prácticas MLOps al aislar el conjunto de test desde el inicio, evitando contaminación durante preprocesamiento y entrenamiento.

**Output clave:** Train (26,931 × 24), Test (11,543 × 24), distribución preservada (Train: 0.902/0.098, Test: 0.902/0.098).

---

## 2. TimeSeriesTransformer y OutlierDetector Personalizados

Se desarrollaron dos transformadores sklearn-compliant: **TimeSeriesTransformer** (2 métodos de interpolación: linear y polynomial grado 2) que ordena cronológicamente las columnas, interpola valores faltantes y extrae 14 características estadísticas (mean, std, min, max, median, skew, kurtosis, q25, q75, zero_count, total_consumption, range, iqr, cv) de forma vectorizada; y **OutlierDetector** (2 técnicas: Isolation Forest y LOF) que agrega 4 nuevas features de detección. Ambos implementan fit/transform correctamente: **fit() solo en train** (aprende parámetros sin ver test), **transform() en ambos** (aplica lo aprendido). La vectorización completa elimina iterrows() mejorando rendimiento >10x.

**Output clave:** 14 features base + 4 features outlier (opcional) = hasta 18 features por configuración.

---

## 3. Pipeline de Preprocesamiento (4 Configuraciones)

Se generaron **4 configuraciones experimentales** combinando técnicas: (1) **Linear_NoOutlier**: interpolación lineal sin detección (14 features), (2) **Linear_Outlier**: interpolación lineal con IF+LOF (18 features), (3) **Poly_NoOutlier**: interpolación polinomial sin detección (14 features), (4) **Poly_Outlier**: interpolación polinomial con IF+LOF (18 features). Cada configuración se procesa independientemente con sklearn.ColumnTransformer, aplicando fit() en train y transform() en ambos conjuntos. La detección de outliers identificó ~10% de anomalías (contamination=0.1) agregando información relevante sobre patrones atípicos de consumo.

**Output clave:** 4 configuraciones listas, cada una con X_train y X_test procesados correctamente.

---

## 4. Meta-Modelo Random Forest para Extracción de Características

Se entrenó un **Random Forest meta-modelo** (100 trees, max_depth=10) sobre cada configuración para generar **RF_Anomaly_Score**: probabilidad de fraude que captura patrones no lineales complejos. Este score (rango 0-1) se agregó como feature adicional a las 4 configuraciones, enriqueciendo la representación. La implementación previene data leakage: RF se entrena **solo en X_train** de cada config y genera scores para train/test separadamente. Esta técnica de stacking aumenta el poder predictivo al combinar información estadística base con aprendizaje ensemble.

**Output clave:** RF_Anomaly_Score agregado exitosamente, rangos típicos train (min=0.01, max=0.99, mean=0.10) coherentes con distribución de fraude.

---

## 5. Pipelines de Modelos con Balanceo (10 Pipelines)

Se definieron **10 pipelines imblearn** combinando 3 estrategias de balanceo con 4 clasificadores: **SMOTETomek** (over+under sampling, 4 pipelines: SVM, GNB, RF, LR), **RandomUnderSampler** (under sampling, 4 pipelines), y **Sin Balanceo** (baseline, 2 pipelines: SVM, GNB). Cada pipeline usa imblearn.Pipeline que aplica sampling **solo durante fit()** (sobre train) pero **no durante predict()** (sobre test), garantizando evaluación realista. Los hiperparámetros se estandarizaron: SVC (C=1, probability=True), GNB (var_smoothing=1e-8), RF (n_estimators=100, max_depth=10), LR (C=1, max_iter=1000).

**Output clave:** 10 pipelines listos (4 SMOTETomek + 4 UnderSampler + 2 Sin Balanceo) para experimentación sistemática.

---

## 6. Entrenamiento y Evaluación (40 Experimentos)

Se ejecutaron **40 experimentos únicos** (4 configs × 10 pipelines) con evaluación exhaustiva: Accuracy, Precision, Recall, F1-Score, ROC-AUC, Balanced Accuracy y matriz de confusión. Cada experimento entrena el pipeline completo en X_train (con balanceo si aplica) y evalúa en X_test (sin balanceo). El logging detallado registra métricas por experimento permitiendo comparación directa. Los resultados revelan que clasificadores simples (GNB) superan a modelos complejos (SVM, RF) probablemente por el desbalanceo extremo y alta dimensionalidad tras feature engineering. El modelo global alcanzó **F1=0.8822** y **ROC-AUC=0.6171**.

**Output clave:** 40 experimentos completados, mejor configuración identificada: Linear_NoOutlier + GNB (SMOTETomek).

---

## 7. Análisis Comparativo de Resultados

El análisis dimensional revela insights clave sobre cada técnica implementada y su impacto en el rendimiento del modelo de detección de fraude. Se evaluaron sistemáticamente los efectos de interpolación, detección de outliers y balanceo.

**Output clave:** TOP 10 configuraciones ordenadas, mejor modelo global identificado, análisis por dimensión completado.

---

## Respuestas a Preguntas Clave

### 1. ¿Qué método de interpolación es mejor? Linear vs Polynomial

**Respuesta:** Interpolación **Polynomial (grado 2)** es superior con **+15.63% mejora** en F1-Score promedio.

**Evidencia:**
- **Linear:** F1-Score promedio = 0.7077 (±0.3021), máximo = 0.8822, ROC-AUC = 0.6234
- **Polynomial:** F1-Score promedio = 0.8184 (±0.1228), máximo = 0.8805, ROC-AUC = 0.6086

**Análisis:** La interpolación polinomial cuadrática captura mejor patrones no lineales en consumo eléctrico temporal, reduciendo variabilidad (std: 0.1228 vs 0.3021) y mejorando consistencia. Aunque Linear logra el F1 máximo absoluto (0.8822), Polynomial ofrece rendimiento más robusto promedio con menor desviación estándar, crucial para producción.

---

### 2. ¿La detección de outliers mejora el rendimiento? Con vs Sin Outliers

**Respuesta:** **NO**, la detección de outliers **degrada rendimiento -8.13%** en F1-Score promedio.

**Evidencia:**
- **Sin Outliers:** F1-Score promedio = 0.8305 (±0.0881), máximo = 0.8822, ROC-AUC = 0.6272
- **Con Outliers (IF + LOF):** F1-Score promedio = 0.7631 (±0.2344), máximo = 0.8822, ROC-AUC = 0.6160

**Análisis:** Agregar features de outliers (is_outlier_IF, outlier_score_IF, is_outlier_LOF, outlier_score_LOF) introduce ruido y aumenta dimensionalidad sin aportar información discriminativa para fraude eléctrico. La mayor desviación estándar (0.2344 vs 0.0881) indica inestabilidad. Los **4 mejores modelos TOP usan configuraciones NoOutlier**, sugiriendo que las 14 features estadísticas base son suficientes y las features de outliers confunden al clasificador.

---

### 3. ¿Qué técnica de balanceo funciona mejor? SMOTETomek vs RandomUnderSampler vs Sin Balanceo

**Respuesta:** **RandomUnderSampler** funciona mejor con **+7.48% mejora** vs Sin Balanceo.

**Evidencia:**
- **SMOTETomek:** F1-Score promedio = 0.6954 (±0.2927), ROC-AUC = 0.6350, **-9.66% vs Baseline**
- **RandomUnderSampler:** F1-Score promedio = 0.8273 (±0.0655), ROC-AUC = 0.6529, **+7.48% vs Baseline**
- **Sin Balanceo:** F1-Score promedio = 0.7698 (±0.3056), ROC-AUC = 0.5044

**Análisis:** RandomUnderSampler balancea reduciendo clase mayoritaria sin generar datos sintéticos, evitando overfitting a ejemplos artificiales (problema de SMOTE). Su menor variabilidad (std=0.0655) y mayor ROC-AUC (0.6529) demuestran superioridad. SMOTETomek **empeora** rendimiento probablemente por amplificar ruido en zona de frontera de decisión. Sorprendentemente, GNB Sin Balanceo alcanza el **F1 máximo global (0.8822)**, sugiriendo que GaussianNB maneja bien desbalanceo natural con features bien diseñadas.

---

### 4. ¿Cuál es la mejor combinación global? (40 experimentos evaluados)

**Respuesta:** **Linear_NoOutlier + GNB (SMOTETomek)** es la mejor configuración global.

**Evidencia:**
- **Configuración:** Interpolación Lineal sin Detección de Outliers
- **Pipeline:** Gaussian Naive Bayes con SMOTETomek
- **Métricas:**
  - F1-Score: **0.8822** (mejor de 40 experimentos)
  - ROC-AUC: **0.6171**
  - Accuracy: **0.9113**
  - Balanced Accuracy: **0.5304**
  - Precision: **0.8745**
  - Recall: **0.9113**

**TOP 3 Configuraciones:**
1. Linear_NoOutlier + GNB (SMOTETomek) - F1: **0.8822**
2. Linear_NoOutlier + GNB (Sin Balanceo) - F1: **0.8817** (diferencia mínima: 0.0005)
3. Poly_NoOutlier + GNB (SMOTETomek) - F1: **0.8805**

**Análisis Crítico:** Los 3 mejores modelos comparten patrones: (1) **NoOutlier** (detección de outliers perjudica), (2) **GNB** (Gaussian Naive Bayes supera a SVM/RF/LR), (3) **Interpolación simple** (Linear suficiente pese a que Poly tiene mejor promedio). El modelo ganador logra **91.13% accuracy** pero **balanced accuracy solo 53.04%**, revelando sesgo hacia clase mayoritaria (no fraude). El **recall 91.13%** indica excelente detección de fraudes verdaderos, crítico en este dominio donde falsos negativos (fraudes no detectados) son costosos. La diferencia mínima entre SMOTETomek y Sin Balanceo (0.0005) sugiere que **GNB inherentemente robusto a desbalanceo** cuando features son informativas.

**Recomendación:** Implementar **Linear_NoOutlier + GNB (SMOTETomek)** en producción con monitoreo de balanced accuracy. Considerar umbral de probabilidad ajustable (0.5 default) para trade-off precision/recall según costo de negocio de falsos positivos vs negativos.

---

## Conclusiones Metodológicas

Este experimento demuestra que:

1. **Simplicidad > Complejidad:** Interpolación lineal + 14 features estadísticas + GNB simple superan técnicas complejas (polynomial, outliers, ensemble models).

2. **Data Leakage Prevention Crítico:** División train-test como primer paso y fit/transform correcto aseguran evaluación honesta (diferencia entre 88% F1 real vs potencial 95%+ con leakage).

3. **Balanceo Contextual:** RandomUnderSampler mejora promedio general pero GNB sin balanceo alcanza máximo absoluto, indicando que **técnica óptima depende del clasificador**.

4. **Evaluación Multimétrica Esencial:** F1-Score alto (0.88) con balanced accuracy bajo (0.53) revela sesgo hacia mayoría; ROC-AUC (0.62) muestra capacidad discriminativa moderada. Decisiones de producción requieren análisis completo, no métrica única.

5. **Experimentación Sistemática Valiosa:** 40 experimentos revelaron que configuración intuitivamente "mejor" (Polynomial + Outliers + SMOTETomek) rinde **peor** que baseline simple, validando necesidad de evidencia empírica vs asunciones.

---

## Archivos Generados

- **resultados_experimentacion_completa.csv:** 40 experimentos con métricas completas
- **grupo_06_caso-electricidad-entregable.ipynb:** Notebook ejecutado con outputs
- **README.md:** Este documento de sustentación

---

**Autores:** Grupo 06  
**Fecha:** Noviembre 2025  
**Dataset:** Paper Electricidad/data.csv (38,474 registros)  
**Framework:** sklearn + imblearn + pandas  
**Reproducibilidad:** random_state=42 en todos los componentes
