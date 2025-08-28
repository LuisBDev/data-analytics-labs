# CAPÍTULO 1: ANÁLISIS DESCRIPTIVO DE DATOS DEL BANCO MUNDIAL (WDI)

## Integrantes del Grupo 6 - Analítica de Datos

- **Balarezo Ramos Luis Jesus**
- **Soller Barrenechea Carlos Javier**  
- **Callupe Arias Jefferson Jesus**
- **Lizarbe Estrada Adrian Jesus**

---

## 1.1 INTRODUCCIÓN Y OBJETIVOS

### 1.1.1 Objetivos del Análisis

El presente análisis descriptivo tiene como objetivo realizar un estudio comprehensivo de los datos del World Development Indicators (WDI) del Banco Mundial, enfocándose en indicadores clave que permitan evaluar el desarrollo económico, social y ambiental de países seleccionados.

### 1.1.2 Indicadores Principales Analizados

1. **PIB per cápita** (USD constantes 2015) - Indicador económico
2. **Esperanza de vida al nacer** (años) - Indicador social/salud  
3. **Población total** - Contexto demográfico
4. **Emisiones CO2 per cápita** (toneladas métricas) - Indicador ambiental
5. **Exports de bienes y servicios** (% del PIB) - Indicador de comercio internacional
6. **Imports de bienes y servicios** (% del PIB) - Indicador de comercio internacional

### 1.1.3 Países Objetivo del Análisis

- **USA** (Estados Unidos), **CAN** (Canadá), **GBR** (Reino Unido), **JPN** (Japón)
- **SGP** (Singapur), **RUS** (Federación Rusa), **IND** (India), **CHN** (China)

### 1.1.4 Cobertura Temporal

- **Serie histórica completa**: 1960-2024 (65 años de datos)
- **Enfoque en años recientes**: 2015-2024 para análisis comparativo actual

---

## 1.2 METODOLOGÍA Y TRANSFORMACIÓN DE DATOS

### 1.2.1 Carga y Estructura Inicial

El dataset original del WDI contenía:
- **403,256 observaciones** iniciales con **69 columnas**
- **266 países/regiones** únicos
- **1,516 indicadores** diferentes
- **65 años** de cobertura temporal (1960-2024)

### 1.2.2 Transformación de Datos

#### Proceso de Reestructuración
Se aplicó una transformación de pivoteo para convertir la estructura original (años como columnas) a formato long:

- **Estructura original**: Años en columnas (1960, 1961, ..., 2024)
- **Estructura transformada**: Variable "Year" con años en filas
- **Resultado**: 26,211,640 observaciones en formato analítico

#### Optimización de Tipos de Datos
- **Year**: Convertido a int16 para eficiencia
- **Value**: Convertido a float32 para valores económicos
- **Encoding**: UTF-8 para compatibilidad internacional

### 1.2.3 Calidad de Datos

#### Valores Faltantes
- **Total de valores faltantes**: 17,253,904 (65.8% del dataset)
- **Causa principal**: Disponibilidad desigual de datos históricos y por país
- **Indicadores con mayor completitud**: Variables demográficas (17,225 observaciones)

#### Consistencia Geográfica
- **266 países únicos** con códigos ISO consistentes
- **Verificación exitosa**: Cada país tiene un código único
- **Cobertura temporal completa**: Sin años faltantes en la serie 1960-2024

---

## 1.3 ANÁLISIS DESCRIPTIVO POR INDICADOR

### 1.3.1 Análisis Económico: PIB per cápita (2023)

#### Estadísticas Descriptivas
- **Países con datos válidos**: 250 de 266 (94.0%)
- **Promedio global**: $16,250 USD
- **Mediana**: $6,429 USD
- **Desviación estándar**: $24,385 USD
- **Coeficiente de variación**: 150.1%

#### Distribución y Extremos
- **Mínimo**: $253 USD (Burundi)
- **Máximo**: $224,582 USD (Monaco)
- **Q1 (25%)**: $2,237 USD
- **Q3 (75%)**: $19,207 USD
- **Rango intercuartílico**: $16,971 USD

#### Interpretación
La gran diferencia entre media y mediana ($16,250 vs $6,429) indica una **distribución altamente sesgada** hacia países con ingresos altos. El coeficiente de variación de 150.1% refleja **extremas desigualdades económicas globales**.

### 1.3.2 Análisis Social: Esperanza de Vida (2023)

#### Estadísticas Descriptivas
- **Países con datos válidos**: 265 de 266 (99.6%)
- **Promedio global**: 73.3 años
- **Mediana**: 73.6 años
- **Desviación estándar**: 6.9 años
- **Coeficiente de variación**: 9.4%

#### Distribución y Extremos
- **Mínimo**: 54.5 años (Nigeria)
- **Máximo**: 86.4 años (Monaco)
- **Q1 (25%)**: 67.7 años
- **Q3 (75%)**: 78.1 años
- **Rango intercuartílico**: 10.4 años

#### Interpretación
La **proximidad entre media y mediana** (73.3 vs 73.6) indica una distribución relativamente simétrica. El menor coeficiente de variación (9.4%) sugiere una **mayor convergencia global en salud** comparado con indicadores económicos.

### 1.3.3 Análisis Demográfico: Población Total (2023)

#### Estadísticas Descriptivas
- **Países con datos válidos**: 265 de 266 (99.6%)
- **Promedio**: 347,859,360 habitantes
- **Mediana**: 11,538,306 habitantes
- **Coeficiente de variación**: 298.8%

#### Distribución y Extremos
- **Mínimo**: 9,816 habitantes (Tuvalu)
- **Máximo**: 8,064,976,384 habitantes (World - agregado)
- **Q1**: 2,481,380 habitantes
- **Q3**: 80,852,048 habitantes

#### Interpretación
La **extrema diferencia entre media y mediana** refleja que pocos países muy poblados elevan significativamente el promedio. El coeficiente de variación de 298.8% es el más alto entre todos los indicadores.

---

## 1.4 ANÁLISIS DE CORRELACIONES

### 1.4.1 Matriz de Correlaciones Principales

| Indicador | PIB per cápita | Esperanza de vida | Población |
|-----------|----------------|-------------------|-----------|
| **PIB per cápita** | 1.000 | 0.628 | -0.099 |
| **Esperanza de vida** | 0.628 | 1.000 | -0.044 |
| **Población** | -0.099 | -0.044 | 1.000 |

### 1.4.2 Interpretación de Correlaciones

#### PIB vs Esperanza de Vida (0.628)
- **Correlación moderada positiva fuerte**
- **Interpretación**: Mayor prosperidad económica se asocia con mejor salud poblacional
- **Implicación**: Inversión en desarrollo económico puede mejorar indicadores de salud

#### PIB vs Población (-0.099)
- **Correlación negativa muy débil**
- **Interpretación**: No existe relación clara entre tamaño poblacional y riqueza per cápita
- **Implicación**: Países pequeños pueden ser prósperos; países grandes pueden ser pobres o ricos

#### Esperanza de Vida vs Población (-0.044)
- **Correlación negativa prácticamente nula**
- **Interpretación**: El tamaño poblacional no determina los niveles de salud
- **Implicación**: Políticas de salud efectivas son independientes del tamaño del país

---

## 1.5 ANÁLISIS AMBIENTAL: EMISIONES DE CO2

### 1.5.1 Datos Disponibles
- **Indicador utilizado**: "Carbon dioxide (CO2) emissions excluding LULUCF per capita (t CO2e/capita)"
- **Países con datos**: 19 de los principales emisores globales
- **Período de análisis**: 1991-2023

### 1.5.2 Estadísticas Descriptivas de Emisiones

#### Distribución General
- **Promedio**: 53.4 toneladas métricas per cápita
- **Mediana**: 17.3 toneladas métricas per cápita
- **Desviación estándar**: 92.4 toneladas métricas per cápita
- **Rango**: -48.1 a 449.2 toneladas métricas per cápita

### 1.5.3 Rankings por Emisiones (2023)

#### Principales Emisores
1. **China**: 449.2 t per cápita 🥇
2. **India**: 392.0 t per cápita 🥇  
3. **Indonesia**: 317.0 t per cápita 🥇
4. **Irán**: 273.6 t per cápita 🥈
5. **Arabia Saudí**: 258.2 t per cápita 🥈
6. **Perú**: 180.2 t per cápita 🥈

#### Menores Emisores
- **Reino Unido**: -48.1 t per cápita
- **Alemania**: -42.5 t per cápita  
- **Francia**: -26.7 t per cápita

### 1.5.4 Análisis Específico de Perú

- **Emisiones CO2 per cápita**: 180.2 toneladas métricas (2023)
- **Posición global**: 6° de 19 países analizados (percentil 68.4%)
- **Tendencia temporal**: Creciente (+6.26 t/año desde 1991)
- **Cambio total**: +183.1 toneladas métricas (1991-2023)
- **Categorización**: Emisor intermedio-alto

---

## 1.6 ANÁLISIS DE COMERCIO INTERNACIONAL

### 1.6.1 Exports de Bienes y Servicios

#### Estadísticas Generales
- **Promedio global**: 39.23% del PIB
- **Mediana**: 20.94% del PIB
- **Desviación estándar**: 54.19% del PIB
- **Coeficiente de variación**: 138.2%

#### Rankings por Exports (Promedio Histórico)
1. **Singapur**: 169.4% del PIB - Economía extremadamente abierta 🌍
2. **Federación Rusa**: 30.1% del PIB - Economía moderada ⚖️
3. **Canadá**: 28.7% del PIB - Economía abierta 📈
4. **Reino Unido**: 26.7% del PIB - Economía abierta 📈
5. **China**: 14.7% del PIB - Economía relativamente cerrada 🔒

### 1.6.2 Imports de Bienes y Servicios

#### Estadísticas Generales
- **Promedio global**: 37.46% del PIB
- **Mediana**: 20.44% del PIB
- **Desviación estándar**: 50.34% del PIB
- **Coeficiente de variación**: 134.4%

#### Correlación Exports-Imports
- **Coeficiente**: 0.992 (correlación fuerte positiva)
- **Interpretación**: Países que exportan más también tienden a importar más
- **Implicación**: El comercio internacional es bidireccional y complementario

### 1.6.3 Balance Comercial por País

#### Países con Superávit Comercial
- **Singapur**: +9.8% del PIB
- **Federación Rusa**: +8.0% del PIB
- **Canadá**: +0.8% del PIB
- **Japón**: +0.7% del PIB

#### Países con Déficit Comercial
- **India**: -1.9% del PIB
- **Estados Unidos**: -1.8% del PIB
- **Reino Unido**: -0.7% del PIB

### 1.6.4 Categorización por Apertura Comercial

- **🌍 Economía extremadamente abierta** (≥100% PIB): Singapur (329.0%)
- **🔓 Economía muy abierta** (60-100% PIB): Ninguna en la muestra
- **📈 Economía abierta** (40-60% PIB): Canadá, Reino Unido, Federación Rusa
- **⚖️ Economía moderadamente abierta** (25-40% PIB): Japón, India, China
- **🔒 Economía relativamente cerrada** (<25% PIB): Estados Unidos (20.0%)

---

## 1.7 ANÁLISIS TEMPORAL Y TENDENCIAS

### 1.7.1 Tendencias de Emisiones CO2 (1991-2023)

#### Países con Tendencia Creciente
- **China**: +15.57 t/año ⬆️ (cambio total: +443.6 t)
- **Perú**: +6.26 t/año ⬆️ (cambio total: +183.1 t)
- **Brasil**: +3.86 t/año ⬆️ (cambio total: +107.6 t)

#### Países con Tendencia Decreciente
- **Alemania**: -0.91 t/año ⬇️ (cambio total: -40.4 t)
- **Estados Unidos**: -0.43 t/año ⬇️ (cambio total: -5.2 t)

### 1.7.2 Tendencias de Comercio Internacional

#### Exports (Cambio Anual Promedio)
- **Singapur**: +1.086% anual ⬆️ (mayor crecimiento)
- **China**: +0.414% anual ⬆️
- **India**: +0.357% anual ⬆️
- **Federación Rusa**: -0.180% anual ⬇️ (única decreciente)

#### Volatilidad de Exports (Coeficiente de Variación)
- **Mayor volatilidad**: India (63.4%), China (63.2%)
- **Menor volatilidad**: Reino Unido (11.2%), Singapur (17.1%)
- **Interpretación**: Economías emergentes muestran mayor variabilidad

---

## 1.8 VISUALIZACIONES DE DATOS

### 1.8.1 Gráfico de Dispersión: PIB vs Esperanza de Vida

#### Descripción de la Visualización
- **Tipo**: Gráfico de dispersión (scatter plot) con tamaño de burbuja
- **Variables**: 
  - Eje X: Esperanza de vida al nacer (años)
  - Eje Y: PIB per cápita (USD constantes 2015)
  - Tamaño de burbuja: Población total
- **Datos**: 250 países con datos completos para 2023

#### Hallazgos Visuales
- **Patrón general**: Correlación positiva visible entre PIB y esperanza de vida
- **Outliers identificados**: 
  - Monaco: PIB extremadamente alto ($224,582) con esperanza de vida alta (86.4 años)
  - Países del Golfo: Alto PIB con esperanza de vida moderada
  - Países africanos: Baja esperanza de vida y bajo PIB
- **Agrupaciones observadas**:
  - Países desarrollados: Esquina superior derecha (alto PIB, alta esperanza de vida)
  - Países en desarrollo: Centro del gráfico
  - Países menos desarrollados: Esquina inferior izquierda

#### Interpretación
La visualización confirma la **relación positiva moderada** (r=0.628) entre prosperidad económica y salud poblacional, pero también revela que otros factores influyen significativamente en la esperanza de vida.

### 1.8.2 Análisis Temporal de Emisiones CO2

#### Configuración de la Visualización
- **Estructura**: Panel de 4 subgráficos (2x2)
- **Período**: 1991-2023 (32 años)
- **Países analizados**: 19 principales emisores globales

#### Subgráfico 1: Principales Emisores de CO2
- **Países incluidos**: Estados Unidos, China, Federación Rusa, Alemania, Japón, Canadá
- **Observaciones clave**:
  - China muestra crecimiento exponencial desde 2000
  - Estados Unidos con tendencia decreciente post-2005
  - Alemania con reducción sostenida desde 1990

#### Subgráfico 2: Emisores Intermedios
- **Países incluidos**: Brasil, México, Turquía, Irán
- **Patrones identificados**:
  - Brasil con crecimiento acelerado reciente
  - México con volatilidad moderada
  - Irán con tendencia creciente constante

#### Subgráfico 3: Perú - Análisis Detallado
- **Características especiales**:
  - Línea de tendencia añadida (pendiente: +6.26 t/año)
  - Valores máximo y mínimo marcados visualmente
  - **Máximo**: 180.2t (2023)
  - **Mínimo**: -2.9t (1991)
- **Interpretación**: Crecimiento sostenido de emisiones correlacionado con desarrollo económico

#### Subgráfico 4: Comparación de Grupos
- **Líneas mostradas**:
  - Promedio de principales emisores (línea roja)
  - Promedio de emisores intermedios (línea naranja)  
  - Perú individual (línea roja específica)
- **Insight principal**: Perú sigue patrón similar a emisores intermedios pero con mayor volatilidad

### 1.8.3 Evolución Temporal del Comercio Internacional

#### Panel Principal: Exports e Imports (4 subgráficos)

#### Subgráfico 1: Evolución de Exports (% del PIB)
- **Patrón destacado**: Singapur como outlier extremo (>150% del PIB)
- **Tendencias observadas**:
  - Singapur: Crecimiento constante hasta 2008, estabilización posterior
  - China: Crecimiento acelerado 1980-2005, estabilización reciente
  - Estados Unidos: Estabilidad en torno al 10-12% del PIB
- **Volatilidad**: Economías pequeñas muestran mayor fluctuación

#### Subgráfico 2: Evolución de Imports (% del PIB)
- **Correlación visual**: Patrones similares a exports en la mayoría de países
- **Observaciones específicas**:
  - Reino Unido: Picos pronunciados durante crisis (2008, Brexit)
  - India: Crecimiento gradual pero sostenido
  - Japón: Tendencia relativamente estable

#### Subgráfico 3: Balance Comercial (Exports - Imports)
- **Línea de referencia**: Eje horizontal en cero para identificar superávit/déficit
- **Patrones por país**:
  - **Superávit persistente**: China (post-2000), Federación Rusa
  - **Déficit estructural**: Estados Unidos, Reino Unido
  - **Equilibrio variable**: Canadá, India, Japón
- **Volatilidad temporal**: Crisis globales visibles en todos los países

#### Subgráfico 4: Correlación Exports vs Imports (2015-2024)
- **Visualización**: Scatter plot con línea de tendencia
- **Correlación observada**: 0.997 (casi perfecta)
- **Interpretación**: Países que exportan más también importan más (economías abiertas)
- **Outliers**: Singapur en extremo superior, países cerrados en inferior izquierdo

### 1.8.4 Análisis Comparativo de Distribuciones

#### Panel Complementario: Distribuciones y Comparaciones

#### Box Plots de Exports por País
- **Visualización**: Diagramas de caja para cada país
- **Hallazgos**:
  - **Mayor dispersión**: Singapur (rango 100-200% PIB)
  - **Mayor estabilidad**: Estados Unidos (rango 8-15% PIB)
  - **Valores atípicos identificados**: Picos en crisis y booms económicos

#### Box Plots de Imports por País
- **Patrones similares** a exports pero con menor dispersión general
- **Observación clave**: Todos los países muestran algunos valores atípicos

#### Gráfico de Barras: Promedios Históricos
- **Formato**: Barras pareadas (exports vs imports) por país
- **Jerarquía visual clara**:
  1. Singapur: Líder absoluto en ambas categorías
  2. Federación Rusa, Canadá, Reino Unido: Apertura moderada
  3. China, Japón, India: Apertura baja-moderada
  4. Estados Unidos: Menor apertura relativa

#### Heatmap de Apertura Comercial (2014-2024)
- **Visualización**: Mapa de calor con valores numéricos
- **Escala de colores**: Viridis (oscuro = menor apertura, claro = mayor apertura)
- **Patrones temporales identificados**:
  - Singapur: Consistentemente alto (300+ % PIB)
  - Tendencias decrecientes post-COVID en varios países
  - Recuperación gradual 2022-2024

### 1.8.5 Insights Principales de las Visualizaciones

#### Patrones Transversales Identificados

1. **Correlaciones fuertes**:
   - PIB vs Esperanza de vida: Visible pero no lineal
   - Exports vs Imports: Casi perfecta (0.997)
   - Desarrollo vs Emisiones: Relación compleja no-lineal

2. **Outliers sistemáticos**:
   - **Singapur**: Economía híper-abierta en comercio
   - **Monaco**: PIB per cápita extremo con alta longevidad
   - **China**: Transformación acelerada en todos los indicadores

3. **Tendencias temporales**:
   - **Globalización visible**: Incremento general en apertura comercial 1990-2008
   - **Crisis globales reflejadas**: 2008, COVID-19 visibles en todas las series
   - **Patrones de recuperación**: Diferentes velocidades por país

4. **Agrupaciones por desarrollo**:
   - **Países desarrollados**: Alto PIB, alta esperanza de vida, apertura moderada
   - **Economías emergentes**: Crecimiento acelerado, mayor volatilidad
   - **Países en desarrollo**: Patrones heterogéneos, menor integración comercial

#### Implicaciones Metodológicas

1. **Calidad de visualizaciones**: 
   - Uso efectivo de color y tamaño para múltiples dimensiones
   - Escalas apropiadas para comparaciones válidas
   - Anotaciones clarificadoras en puntos clave

2. **Limitaciones identificadas**:
   - Agregaciones nacionales pueden ocultar disparidades internas
   - Datos más recientes pueden ser preliminares
   - Outliers extremos pueden distorsionar escalas

3. **Valor analítico**:
   - Confirmación visual de correlaciones estadísticas
   - Identificación de patrones temporales complejos
   - Revelación de casos excepcionales para investigación adicional

---

## 1.9 CONCLUSIONES DEL ANÁLISIS DESCRIPTIVO

### 1.9.1 Hallazgos Principales por Dimensión

#### Dimensión Económica
- **Desigualdades extremas**: Diferencia de 900 veces entre países más ricos y pobres
- **Concentración de riqueza**: 50% de países con PIB per cápita menor a $6,429
- **Desarrollo heterogéneo**: Múltiples modelos de desarrollo económico exitoso

#### Dimensión Social  
- **Convergencia en salud**: Menor variabilidad que indicadores económicos
- **Relación PIB-Salud**: Correlación moderada (0.628) sugiere otros factores importantes
- **Logros relativos**: Países con PIB bajo pueden alcanzar esperanza de vida alta

#### Dimensión Ambiental
- **Patrones diversos**: Emisiones CO2 no correlacionan directamente con desarrollo
- **Oportunidades de eficiencia**: Algunos países logran prosperidad con bajas emisiones
- **Tendencias preocupantes**: Países emergentes con emisiones crecientes

#### Dimensión Comercial
- **Apertura diferenciada**: Desde economías cerradas (EE.UU.) hasta extremadamente abiertas (Singapur)  
- **Especialización regional**: Diferentes modelos de inserción comercial global
- **Complementariedad**: Alta correlación entre exports e imports (0.992)

### 1.9.2 Patrones Temporales Identificados

1. **Serie histórica robusta**: 65 años permiten análisis de tendencias a largo plazo
2. **Evolución diferenciada**: Cada país muestra trayectorias únicas de desarrollo
3. **Eventos globales visibles**: Crisis y cambios de política reflejados en los datos
4. **Tendencias emergentes**: Indicios de posible desarrollo sostenible en algunos casos

### 1.9.3 Implicaciones para Políticas de Desarrollo

#### Desarrollo Económico
- **Múltiples vías**: No existe un modelo único de desarrollo exitoso
- **Tamaño no determina éxito**: Países pequeños pueden ser muy prósperos
- **Importancia de eficiencia**: Optimización de recursos vs simple acumulación

#### Desarrollo Social
- **Inversión en salud pública**: Políticas específicas pueden ser más efectivas que solo crecimiento económico
- **Equidad vs crecimiento**: Balance necesario entre ambos objetivos

#### Desarrollo Ambiental
- **Desacoplamiento posible**: Algunos países logran desarrollo con bajas emisiones
- **Urgencia de políticas**: Países emergentes necesitan estrategias de desarrollo limpio
- **Oportunidades tecnológicas**: Transferencia de tecnología verde puede acelerar transición

#### Integración Comercial
- **Apertura gradual**: Diferentes niveles de integración comercial pueden ser exitosos
- **Especialización inteligente**: Enfoque en ventajas comparativas vs diversificación total
- **Balance comercial**: Superávit/déficit sostenible según contexto económico específico

---

## 1.10 LIMITACIONES Y CONSIDERACIONES METODOLÓGICAS

### 1.10.1 Limitaciones de los Datos
- **Valores faltantes significativos**: 65.8% en algunos indicadores
- **Calidad variable**: Sistemas estadísticos heterogéneos entre países
- **Comparabilidad temporal**: Cambios metodológicos a lo largo del tiempo

### 1.10.2 Consideraciones Analíticas
- **Análisis descriptivo**: Sin inferencia causal entre variables
- **Agregaciones**: Datos nacionales pueden ocultar disparidades internas
- **Contexto temporal**: Datos de 2023-2024 pueden ser preliminares

### 1.10.3 Preparación para Análisis Avanzado
- **Dataset exportado**: 17,195 registros con 6 variables principales listos para Power BI
- **Cobertura temporal completa**: 1960-2024 para análisis longitudinal
- **Optimización realizada**: Tipos de datos y estructura apropiados para análisis posterior

---

**Nota**: Este análisis descriptivo constituye la base para análisis más profundos de correlaciones, causalidad y modelado predictivo en fases posteriores del proyecto de analítica de datos.
