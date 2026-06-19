# Changelog

Todos los cambios relevantes del proyecto se documentan en este archivo.

## [Fase 4] - 2026-06-19

### Notebook

#### Added
- Se incorporaron visualizaciones analíticas para comunicar los principales hallazgos del dataset procesado.
- Se agregó la distribución de la variable objetivo `Outcome`.
- Se añadieron comparaciones de variables clínicas entre los grupos `Outcome = 0` y `Outcome = 1`.
- Se incorporó una matriz de correlación para revisar asociaciones lineales entre las variables clínicas.
- Se agregaron interpretaciones con enfoque de storytelling, conectando contexto, hallazgos y limitaciones.
- Se incluyeron títulos, etiquetas y explicaciones para facilitar la lectura de los gráficos.

#### Changed
- Se reorganizó el notebook para mantener un flujo claro entre carga de datos, validación, visualización e interpretación.
- Se ajustaron las celdas Markdown para mantener coherencia con los objetivos y resultados de las fases anteriores.
- Se reforzó la explicación del preprocesamiento aplicado antes de generar las visualizaciones.
- Se actualizaron las rutas relativas para trabajar con los archivos procesados del proyecto.
- Se mejoró la presentación de resultados para evitar conclusiones causales no respaldadas por los datos.

#### Validated
- Se verificó que el dataset utilizado para las visualizaciones no contenga nulos en las variables base.
- Se comprobó la ausencia de registros duplicados.
- Se validó que `Outcome` conserve los valores binarios `0` y `1`.
- Se revisó la ejecución secuencial del notebook mediante `Restart & Run All`.

### `utils.py`

#### Added
- Se incorporó una clase especializada para centralizar la generación de visualizaciones.
- Se agregaron métodos para graficar la distribución de `Outcome`, comparar variables clínicas y construir la matriz de correlación.
- Se incluyeron validaciones para comprobar que el `DataFrame` y las columnas requeridas existan antes de graficar.
- Se añadieron docstrings y comentarios para explicar el propósito de las clases y métodos.

#### Changed
- Se mantuvo separada la lógica de visualización respecto del notebook.
- Se reutilizó la arquitectura orientada a objetos implementada en la Fase 3.
- Se mejoró la separación de responsabilidades entre preprocesamiento, validación y visualización.
- Se ajustó el módulo para facilitar la incorporación de nuevos gráficos sin duplicar código en el notebook.
- Se conservaron parámetros claros y retornos consistentes para mantener un flujo legible y mantenible.

---

## [Fase 3] - 2026-06-14

### Notebook
- Se migró el pipeline funcional de la Fase 2 a una implementación orientada a objetos.
- Se incorporó `method chaining` para ejecutar las transformaciones en el orden del flujo de datos.
- Se agregó una comparación de rendimiento entre una solución iterativa y una vectorizada mediante `timeit`.
- Se incorporó la auditoría recursiva de la estructura de carpetas del proyecto.
- Se documentaron los resultados de complejidad temporal y las decisiones de optimización.

### `utils.py`
- Se crearon las clases `PreprocesadorBase` y `PreprocesadorDiabetes`.
- Se aplicaron herencia, encapsulamiento y polimorfismo.
- Se trasladaron las funciones de limpieza y transformación a métodos de clase.
- Se añadió la función `auditar_carpetas_recursivo`.
- Se mantuvieron validaciones mediante `assert` para controlar nulos, duplicados, tipos y escalamiento.
- Se conservaron docstrings y comentarios para facilitar el mantenimiento del código.

---

## [Fase 2] - 2026-06-10

### Notebook
- Se implementó el pipeline completo de preprocesamiento.
- Se agregó la limpieza de valores inválidos y registros duplicados.
- Se incorporó la imputación de valores faltantes mediante la mediana.
- Se crearon variables derivadas a partir de `Age` y `BMI`.
- Se aplicó codificación de variables categóricas y escalamiento de variables numéricas.
- Se exportó el dataset procesado a `data/processed`.

### `utils.py`
- Se centralizaron las funciones reutilizables del pipeline.
- Se definieron funciones con parámetros claros para carga, diagnóstico, limpieza, imputación, transformación, validación y exportación.
- Se incorporó conversión de tipo para `BloodPressure`.
- Se añadieron validaciones de rangos, nulos, duplicados y consistencia de `Outcome`.
- Se incluyó `StandardScaler` para estandarizar las variables numéricas.

---

## [Fase 1] - 2026-06-05

### Notebook
- Se creó el flujo inicial de carga y diagnóstico del dataset.
- Se revisaron dimensiones, tipos de datos, valores nulos, duplicados y distribución de `Outcome`.
- Se estableció el uso de rutas relativas y la conservación del dataset original.
- Se documentó el entorno reproducible y la estructura inicial del repositorio.

### `utils.py`
- Se definieron las primeras funciones de apoyo para la carga y exploración de datos.
- Se estableció una separación inicial entre el notebook y el código reutilizable.
