# Fase 3 - Programación Orientada a Objetos, Recursividad y Eficiencia Algorítmica

## Descripción general

Esta carpeta contiene el desarrollo correspondiente a la **Fase 3** del proyecto del curso **MCDI500 - Programación para Ciencia de Datos**.

El objetivo principal de esta fase es construir el núcleo algorítmico del proyecto, integrando programación estructurada, programación recursiva, medición de eficiencia computacional y programación orientada a objetos aplicada al dataset de diabetes trabajado desde la Fase 2.

El trabajo se desarrolla sobre un flujo reproducible de carga, limpieza, transformación, validación y exportación de datos, incorporando además clases, herencia, polimorfismo, encapsulamiento y mediciones de complejidad.

---

## Estructura de la carpeta F3

```text
F3/
├── data/
│   ├── raw/
│   │   └── diabetes_raw.csv
│   └── processed/
│       └── .gitkeep
├── docs/
├── notebooks/
│   └── F3_Preprocesamiento.ipynb
├── reports/
├── src/
│   └── utils.py
└── README.md
```

---

## Dataset utilizado

El dataset utilizado en esta fase corresponde a un archivo de diabetes almacenado en:

```text
F3/data/raw/diabetes_raw.csv
```

Este archivo contiene variables clínicas asociadas al análisis de diabetes, tales como:

* Pregnancies
* Glucose
* BloodPressure
* SkinThickness
* Insulin
* BMI
* DiabetesPedigreeFunction
* Age
* Outcome

La variable `Outcome` representa la condición diagnóstica objetivo, mientras que las demás variables corresponden a atributos clínicos y biométricos utilizados para el análisis y preprocesamiento.

---

## Notebook principal

El notebook principal de la Fase 3 se encuentra en:

```text
F3/notebooks/F3_Preprocesamiento.ipynb
```

Este notebook integra las siguientes etapas:

1. Carga del dataset desde `F3/data/raw/`.
2. Exploración inicial de los datos.
3. Limpieza y preprocesamiento del dataset.
4. Manejo de valores nulos, valores inválidos y duplicados.
5. Conversión de tipos de datos.
6. Creación de variables derivadas.
7. Codificación de variables categóricas.
8. Escalamiento de variables numéricas.
9. Validación técnica del dataset procesado.
10. Implementación de algoritmos recursivos.
11. Medición de eficiencia con `timeit`.
12. Comparación entre implementaciones alternativas.
13. Refactorización del flujo mediante programación orientada a objetos.
14. Exportación del dataset procesado.

---

## Scripts utilizados

El archivo principal de funciones y clases se encuentra en:

```text
F3/src/utils.py
```

Este archivo contiene funciones reutilizables para:

* Cargar datos.
* Explorar el dataset.
* Convertir tipos de datos.
* Reemplazar valores inválidos.
* Eliminar duplicados.
* Imputar valores faltantes.
* Crear variables derivadas.
* Codificar variables categóricas.
* Escalar variables numéricas.
* Validar el dataset final.
* Auditar carpetas de forma recursiva.
* Encapsular el flujo mediante clases.

La separación del código en `src/utils.py` permite mejorar la organización, reutilización, trazabilidad y mantenibilidad del proyecto.

---

## Programación funcional y estructurada

La primera parte del desarrollo se basa en funciones independientes con responsabilidades específicas.
Cada función cumple una tarea concreta dentro del flujo de trabajo, permitiendo mantener alta cohesión y bajo acoplamiento.

Ejemplos de funciones utilizadas:

```python
cargar_datos()
explorar_dataset()
castear_bloodpressure()
reemplazar_invalidos()
eliminar_duplicados()
imputar_mediana()
crear_variables_derivadas()
codificar_categoricas()
escalar_variables()
validar_dataset_final()
```

Este enfoque permite construir un flujo de entrada, procesamiento y salida de datos de forma clara y verificable.

---

## Preprocesamiento del dataset

El preprocesamiento aplicado considera las siguientes acciones:

1. Lectura del archivo CSV original.
2. Revisión de dimensiones, tipos de datos y valores faltantes.
3. Conversión de variables a tipos adecuados.
4. Reemplazo de valores clínicamente inválidos por valores nulos.
5. Eliminación de registros duplicados.
6. Imputación de valores faltantes mediante la mediana.
7. Creación de variables derivadas.
8. Codificación de variables categóricas.
9. Escalamiento de variables numéricas.
10. Validación final del dataset procesado.

La imputación mediante mediana se utiliza porque es una medida robusta frente a valores extremos, especialmente en variables clínicas como glucosa, presión arterial, insulina e índice de masa corporal.

---

## Recursividad

La Fase 3 incorpora algoritmos recursivos para cumplir con el núcleo algorítmico solicitado.

Entre los procedimientos implementados se consideran:

* Ordenamiento recursivo mediante Merge Sort.
* Búsqueda binaria recursiva.
* Auditoría recursiva de la estructura de carpetas del proyecto.

Estos algoritmos permiten aplicar el enfoque de división del problema en subproblemas más pequeños, incorporando casos base y llamadas recursivas controladas.

---

## Eficiencia y complejidad algorítmica

El notebook incorpora mediciones reproducibles de tiempo de ejecución mediante `timeit`.

Se comparan distintas implementaciones para evaluar eficiencia, por ejemplo:

* Bucle tradicional versus operación vectorizada con Pandas.
* Búsqueda lineal versus búsqueda binaria.
* Merge Sort implementado manualmente versus funciones optimizadas de Python.

Las mediciones permiten interpretar el comportamiento computacional de cada solución y relacionarlo con su complejidad algorítmica.

---

## Programación Orientada a Objetos

La fase incorpora programación orientada a objetos para organizar el flujo de preprocesamiento y transformación de datos.

Los principales conceptos aplicados son:

### Encapsulamiento

El estado del dataset se protege dentro de clases, evitando modificar directamente los datos desde fuera de la estructura definida.

### Herencia

Se define una clase base o contrato común para transformadores, desde la cual heredan clases especializadas.

### Polimorfismo

Distintas clases pueden ser ejecutadas mediante una misma interfaz, permitiendo que el pipeline procese diferentes transformaciones de manera uniforme.

### Composición

El pipeline se construye mediante una lista de etapas, donde cada etapa representa una transformación aplicada al dataset.

---

## Flujo general del procesamiento

El flujo general de trabajo es:

```text
F3/data/raw/diabetes_raw.csv
        ↓
Carga del dataset
        ↓
Exploración inicial
        ↓
Limpieza y preprocesamiento
        ↓
Validación técnica
        ↓
Aplicación de algoritmos recursivos
        ↓
Medición de eficiencia
        ↓
Pipeline orientado a objetos
        ↓
F3/data/processed/diabetes_procesado.csv
```

---

## Salida esperada

El resultado final del procesamiento se exporta en:

```text
F3/data/processed/diabetes_procesado.csv
```

Este archivo corresponde al dataset limpio, transformado y validado, listo para ser utilizado en etapas posteriores del proyecto.

---

## Validación técnica

El notebook incorpora validaciones mediante:

* Revisión de nulos.
* Revisión de duplicados.
* Verificación de tipos de datos.
* Validación de dimensiones.
* Pruebas con `assert`.
* Manejo de excepciones.
* Casos normales, casos límite y casos de error.

Estas validaciones permiten verificar que el flujo de procesamiento sea reproducible y técnicamente consistente.

---

## Reproducibilidad

Para ejecutar correctamente la Fase 3 se recomienda:

1. Clonar el repositorio.
2. Verificar que el archivo `diabetes_raw.csv` esté ubicado en `F3/data/raw/`.
3. Abrir el notebook ubicado en `F3/notebooks/`.
4. Ejecutar el notebook completo mediante `Restart & Run All`.
5. Confirmar que se genere el archivo procesado en `F3/data/processed/`.

---

## Requisitos principales

Las principales librerías utilizadas son:

```text
pandas
numpy
scikit-learn
timeit
tracemalloc
pathlib
```

Estas dependencias permiten la manipulación de datos, transformación de variables, escalamiento, medición de eficiencia y manejo de rutas del proyecto.

---

## Relación con la Fase 2

La Fase 3 se construye a partir del trabajo desarrollado en Fase 2.
El preprocesamiento funcional de F2 se reorganiza y amplía mediante clases, métodos y un pipeline orientado a objetos.

De esta manera, la Fase 3 no reemplaza la Fase 2, sino que la transforma en una arquitectura más modular, reutilizable y escalable.

---

## Estado de avance

La carpeta F3 contiene los componentes necesarios para responder los criterios principales de la Sumativa 3:

* Codificación funcional.
* Preprocesamiento del dataset.
* Validación técnica.
* Eficiencia y optimización.
* Diseño estructurado.
* Recursividad.
* Programación orientada a objetos.
* Documentación técnica.
* Organización del repositorio.
* Notebook ejecutable.

---

## Licencia

La licencia general del proyecto se encuentra definida en el archivo `LICENSE` ubicado en la raíz del repositorio.
