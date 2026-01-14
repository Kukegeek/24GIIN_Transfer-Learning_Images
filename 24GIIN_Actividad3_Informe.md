# Análisis de Robustez y Convergencia Semántica en la Clasificación de Alimentos

**Autor:** Jesús Navarro Cuquejo  
**Universidad:** Universidad Internacional de Valencia  
**Lugar/Fecha:** Murcia, enero de 2026

## Resumen

El presente estudio investiga la relación entre el volumen de datos de entrenamiento y la precisión en modelos de clasificación de imágenes gastronómicas. Se entrenaron cinco instancias de redes neuronales convolucionales variando el tamaño de la muestra (10, 20 y 30 imágenes por categoría) para discriminar entre cinco clases: sopa, plato principal, ensalada, postre y no-comida. Los resultados experimentales demuestran que incrementar el dataset de 10 a 20 muestras reduce significativamente la varianza y mejora la precisión global del 88% al 92%. Sin embargo, un incremento posterior a 30 muestras muestra rendimientos decrecientes, estancándose en un 92% de precisión global. El análisis de errores revela una confusión semántica persistente entre las clases "plato principal" y "postre", sugiriendo que la similitud visual es un factor limitante superior al tamaño de la muestra en volúmenes pequeños.

## I. Introducción

El reconocimiento visual de alimentos es un dominio complejo dentro de la visión por computador, caracterizado por objetos deformables y una falta de estructura rígida definida [1]. A diferencia de la clasificación de objetos industriales, los platos de comida presentan variaciones significativas en presentación, iluminación y composición, dificultando la generalización de los modelos a nuevos datos no vistos. Este desafío de generalización desde datos limitados es un problema central abordado en la teoría moderna de la Inteligencia Artificial [2].

Un obstáculo crítico para la implementación de estos sistemas es la dependencia de grandes volúmenes de datos etiquetados. Este trabajo se centra en cuantificar el rendimiento en regímenes de escasez de datos (*Low-Data Regimes*), con el objetivo de determinar el tamaño de muestra mínimo necesario para obtener predicciones robustas y analizar la naturaleza de los errores persistentes.

## II. Metodología Experimental

### A. Caracterización del Conjunto de Datos

El estudio utilizó un conjunto de datos balanceado compuesto por imágenes RGB redimensionadas a 224 x 224 píxeles. La taxonomía del conjunto incluye cinco clases disjuntas:

1. **Sopa (Soup)**
2. **Plato Principal (Main)**
3. **Ensalada (Salad)**
4. **Postre (Dessert)**
5. **No Comida (Nofood)**

### B. Diseño Experimental

Se diseñó un protocolo experimental incremental para evaluar la sensibilidad del modelo al tamaño del conjunto de entrenamiento:

- **Modelo 10 (A, B, C) (n=10):** Se entrenaron tres modelos independientes con inicialización aleatoria para evaluar la varianza y la estabilidad del aprendizaje con datos mínimos. Con subconjuntos de las 30 muestras disponibles, dando lugar a 3 conjuntos disjuntos.
- **Modelo 20_samples (n=20):** Modelo entrenado con un incremento del 100% en el volumen de datos.
- **Modelo 30_samples (n=30):** Modelo entrenado con el máximo volumen disponible.

### C. Protocolo de Validación

La evaluación se realizó sobre un conjunto de prueba estático de 50 imágenes (10 muestras por clase), completamente independientes del conjunto de entrenamiento. Para garantizar la validez externa, las muestras de prueba fueron seleccionadas maximizando la diversidad en cromatismo, ángulo de visión y composiciones de escenas; en todas las validaciones se usaron el mismo conjunto de muestras, asegurando que las métricas de precisión obtenidas sean directamente comparables entre sí [3].

## III. Resultados Cuantitativos

La **Tabla I** resume el rendimiento cuantitativo. Para la evaluación del desempeño se utilizaron métricas estándar de clasificación supervisada, enfocándose principalmente en la precisión (*accuracy*) como indicador de la capacidad de generalización del modelo [4].

Se observa un comportamiento asintótico en dicha métrica, donde el salto de n=10 a n=20 produce una mejora significativa, mientras que el incremento a n=30 no reporta ganancias cuantitativas adicionales.

**Tabla I. Rendimiento Global por Configuración de Modelo**

| Modelo            | Muestras (n) | Aciertos (Max -> 50) | Precisión |
|:------------------|:------------:|:--------------------:|:---------:|
| Modelo 10_A       |      10      |          45          |  90.00%   |
| Modelo 10_B       |      10      |          44          |  88.00%   |
| Modelo 10_C       |      10      |          43          |  86.00%   |
| Modelo 20_samples |      20      |          46          |  92.00%   |
| Modelo 30_samples |      30      |          46          |  92.00%   |

En la Tabla I se muestra cómo la ganancia de rendimiento se aplana después de las 20 muestras. Esto indica que las 10 muestras adicionales del modelo 30_samples no aportaron suficiente varianza informativa para resolver los casos límite restantes, un fenómeno común en el aprendizaje profundo cuando se alcanza la capacidad de generalización del modelo para un dataset dado [2].

## IV. Discusión

### A. Análisis de modelos con diferentes muestras (n=10)

Los resultados obtenidos con diferentes modelos de 10 muestras demuestran una alta sensibilidad a las condiciones iniciales del entrenamiento. Esta inestabilidad es consistente con los fundamentos teóricos del aprendizaje automático descritos por Russell y Norvig [2], donde la aproximación de funciones complejas con escasas observaciones (muestras, n=10) conduce inevitablemente a una alta varianza y un pobre desempeño fuera de la muestra.

Se destaca la volatilidad en la categoría no comida (**Tabla II**). Mientras que los modelos A y C clasificaron correctamente el 100% de las muestras, el modelo B presentó una degradación del 20%. Esta disparidad confirma que, con n=10, los modelos no convergen hacia una solución generalizable robusta.

**Tabla II. Matriz de Variabilidad Inter-Modelo (n=10)**

| Categoría       | Modelo A | Modelo B | Modelo C | Rango de dispersión (Delta) |
|:----------------|--:|--:|--:|:----------------------------|
| Sopa            |      80% |      90% |      90% | 10%                         |
| Plato principal |      90% |      80% |      70% | 20% (Crítico)               |
| Ensalada        |     100% |     100% |      90% | 10%                         |
| Postre          |      80% |      90% |      80% | 10%                         |
| No Comida       |     100% |      80% |     100% | 20% (Crítico)               |

Al analizar los errores acumulados en la categoría plato principal, se determinó que el 66% de los falsos negativos fueron clasificados erróneamente como postre. Esto sugiere que la red identifica estructuras complejas, pero carece de la resolución para diferenciar clases semánticamente cercanas.

### B. Barrera semántica en modelos más robustos (n=20, n=30)

Al evaluar los modelos se identifica una limitación cualitativa. La **Tabla III** ilustra que el 75% de los errores totales se concentran en la confusión binaria entre plato principal y postre. La persistencia de este error, independientemente del aumento de datos, apunta a una homografía visual que requiere mecanismos de atención más sofisticados.

**Tabla III. Distribución de errores en modelos convergentes (n = 20, n=30)**

| Categoría real | Fallos (n=20) | Fallos (n=30) | Total acumulado | Etiología del error principal |
|:------------------------------|:-------------:|:-------------:|:---------------:|:-----------------------------|
| Plato principal               |       2       |       1       |        3        | Confusión con postre (66%)   |
| Postre                        |       1       |       2       |        3        | Confusión con principal (66%)|
| Sopa                          |       1       |       1       |        2        | Plato principal / ensalada   |
| Ensalada                      |       0       |       0       |        0        | -                            |
| No Comida                     |       0       |       0       |        0        | -                            |
| **TOTAL**                     |     **4**     |     **4**     |      **8**      | Predominancia de error semántico |

## V. Conclusiones

Este estudio permite establecer dos conclusiones sobre redes neuronales profundas [2]:

1. **Umbral de estabilidad:** Se determina empíricamente que n=20 muestras por clase constituye el umbral mínimo para eliminar la varianza crítica observada en modelos de n=10.
2. **Complejidad semántica:** El aumento de datos a n=30 no resolvió la confusión entre plato principal y postre. Esto indica que el problema no es meramente cuantitativo, sino de representación del conocimiento visual. La mayoría de los errores en este estudio provienen de la confusión entre estas dos clases. Esto se debe probablemente a que ambos tipos de comida comparten características visuales de bajo nivel (platos redondos, comida centrada, objetos adyacentes…), un problema que las arquitecturas residuales [1] pueden tener dificultades para desambiguar sin datos adicionales. Aumentar el dataset a 30 muestras no resolvió este problema.

Para resolver estos problemas, habrá que priorizar la calidad sobre la cantidad para estas clases conflictivas, o implementar mecanismos de atención visual que puedan detectar características específicas (texturas de azúcar, tipos de cubiertos) que diferencian un postre de un plato principal.

## Referencias

[1] K. He, X. Zhang, S. Ren, y J. Sun, "Deep Residual Learning for Image Recognition," *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2016, pp. 770–778.

[2] S. Russell y P. Norvig, *Artificial Intelligence: A Modern Approach*, 4a ed. Hoboken, NJ: Pearson, 2020.

[3] O. Russakovsky et al., "ImageNet Large Scale Visual Recognition Challenge," *International Journal of Computer Vision (IJCV)*, vol. 115, no. 3, pp. 211–252, 2015.

[4] Fayrix, "Métricas de evaluación de modelos de Machine Learning," [En línea]. Disponible: https://fayrix.com/machine-learning-metrics_es.
