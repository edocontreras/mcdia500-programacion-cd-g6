# Fase 4 - Visualización, Análisis y Comunicación de Resultados

## Descripción general

Esta carpeta contiene el desarrollo de la **Fase 4** del proyecto del curso **MCDI500 - Programación para la Ciencia de Datos**.

El objetivo de esta fase es integrar el trabajo realizado en las fases anteriores y comunicar los principales hallazgos del dataset de diabetes mediante visualizaciones claras, reproducibles y alineadas con los objetivos del proyecto.

La Fase 4 utiliza el dataset previamente limpiado, transformado y validado. A partir de este resultado se construyen gráficos orientados a identificar patrones, comparar grupos y revisar asociaciones entre las variables clínicas y la variable objetivo `Outcome`.

---

## Estructura de la carpeta F4

```text
F4/
├── data/
│   ├── raw/
│   └── processed/
|       └── diabetes_processed.csv
├── docs/
├── notebooks/
│   └── F4_Visualizaciones.ipynb
├── reports/
├── src/
│   └── utils.py
├── changelog.md
├── requirements.txt
└── README.md
```

La estructura separa los datos, el código reutilizable, el notebook, la documentación y los resultados.

---

## Dataset utilizado

Las visualizaciones se construyen a partir del dataset procesado en las fases anteriores.

Ruta esperada:

```text
F4/data/processed/diabetes_processed.csv
```

Variables principales:

- `Pregnancies`
- `Glucose`
- `BloodPressure`
- `Insulin`
- `BMI`
- `DiabetesPedigreeFunction`
- `Age`
- `Outcome`

La variable `Outcome` representa la condición objetivo:

- `0`: registro sin diagnóstico de diabetes.
- `1`: registro con diagnóstico de diabetes.

---

## Notebook principal

El notebook principal se encuentra en:

```text
F4/notebooks/F4_Visualizaciones.ipynb
```

El flujo incluye:

1. Configuración del entorno y rutas.
2. Carga del dataset procesado.
3. Verificación de estructura, nulos y duplicados.
4. Ejecución del pipeline.
5. Validación del dataset final.
6. Medición de eficiencia con `timeit`.
7. Generación de visualizaciones.
8. Interpretación de resultados.
9. Conclusiones.

Las celdas se organizan de forma secuencial e incluyen explicaciones en Markdown, resultados intermedios y salidas verificables.

---

## Archivo `utils.py`

La lógica reutilizable se encuentra en:

```text
F4/src/utils.py
```

Este archivo concentra:

- Carga y validación de datos.
- Limpieza de valores inválidos.
- Conversión de tipos.
- Imputación de valores faltantes.
- Eliminación de duplicados.
- Creación de variables derivadas.
- Escalamiento.
- Validación técnica.
- Auditoría recursiva de carpetas.
- Clases de preprocesamiento.
- Métodos de visualización.

Esta separación permite que el notebook se concentre en coordinar la ejecución y presentar resultados.

---

## Programación Orientada a Objetos

### `PreprocesadorBase`

Concentra los atributos y comportamientos comunes del pipeline, como la ruta de entrada, el DataFrame original y la copia de trabajo.

### `PreprocesadorDiabetes`

Hereda de `PreprocesadorBase` y aplica reglas específicas del dataset de diabetes. La redefinición de `procesar_especifico()` representa polimorfismo por sobrescritura.

### `VisualizadorDiabetes`

Recibe un DataFrame procesado, valida las columnas requeridas y expone métodos independientes para cada gráfico. Esto evita duplicar código y facilita incorporar nuevas visualizaciones.

---

## Preprocesamiento previo a las visualizaciones

Antes de graficar, el pipeline aplica:

1. Conversión de `BloodPressure` a tipo numérico.
2. Reemplazo de valores clínicamente inválidos.
3. Eliminación de duplicados.
4. Imputación mediante mediana.
5. Creación de variables derivadas.
6. Codificación de variables categóricas.
7. Estandarización con `StandardScaler`.
8. Validación final mediante `assert`.

El dataset final debe quedar sin nulos en las variables base, sin duplicados y con `Outcome` como variable binaria.

---

## Visualizaciones analíticas

La Fase 4 incorpora tres visualizaciones principales:

1. **Gráfico de barras de `Outcome`:** muestra la distribución de los registros con y sin diagnóstico de diabetes.
2. **Boxplots de variables clínicas por `Outcome`:** comparan `Glucose`, `BMI` y `Age` entre los grupos `Outcome = 0` y `Outcome = 1`.
3. **Matriz de correlación:** permite revisar las asociaciones lineales entre las variables clínicas y `Outcome`.

Cada visualización incluye título, ejes, leyenda cuando corresponde, fuente e interpretación analítica.

---

## Storytelling de datos

Las visualizaciones siguen una secuencia narrativa:

```text
Contexto
    ↓
Distribución de Outcome
    ↓
Comparación entre grupos
    ↓
Relaciones entre variables
    ↓
Hallazgos y limitaciones
```

Así, los gráficos se presentan como parte de una historia analítica y no como elementos aislados.

---

## Resultados principales

El análisis permite identificar:

- Un desbalance moderado entre las clases de `Outcome`.
- Valores relativos más altos de `Glucose`, `BMI` y `Age` en el grupo con diabetes.
- Una asociación lineal mayor de `Outcome` con `Glucose` y `BMI`.
- Diferencias entre grupos que pueden orientar una etapa posterior de modelamiento.

Los resultados son exploratorios y no permiten establecer causalidad.

---

## Validación técnica

El proyecto incorpora validaciones para:

- Casos normales de carga, transformación y exportación.
- Casos límite, como ceros inválidos, valores extremos y columnas degradadas.
- Excepciones por rutas inexistentes o archivos vacíos.
- Ausencia de nulos y duplicados.
- Consistencia de `Outcome`.
- Coherencia dimensional.
- Correcta estandarización.
- Existencia de columnas antes de graficar.

Los resultados intermedios se comprueban mediante mensajes por consola, tablas, `df.info()`, conteos y salidas visibles en las celdas.

---

## Eficiencia y optimización

La Fase 3 comparó la limpieza de `BloodPressure` mediante un bucle fila por fila y una operación vectorizada con Pandas.

```text
Enfoque iterativo:   60,7 ms
Enfoque vectorizado: 1,42 ms
Aceleración:         42,74 veces
```

Ambas alternativas presentan complejidad temporal O(n), pero se eligió la solución vectorizada por su menor sobrecarga y mejor rendimiento.

Nota: Estos números son representativos de la ejecución realizada por el grupo, sin embargo van a variar, 
para quien ejecuté el notebook, no obstante se comprobará cuando se ejecuté que el resultado será similar y no variará significativamente.

---

## Reproducibilidad

```powershell
git clone https://github.com/MagUnab/mcdia500-programacion-cd-g6.git
cd mcdia500-programacion-cd-g6/F4
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name mcdia500-g6 --display-name "Python 3.12 - MCDIA500 G6"
python -m jupyterlab --ServerApp.use_redirect_file=False
```

Luego:

1. Abrir el notebook de `F4/notebooks/`.
2. Seleccionar el kernel configurado.
3. Ejecutar `Restart & Run All`.
4. Confirmar que finalice sin errores.
5. Verificar que los resultados coincidan con el informe.

---

## Requisitos principales

```text
pandas
numpy
matplotlib
seaborn
scikit-learn
jupyterlab
ipykernel
```

`pathlib` forma parte de la biblioteca estándar de Python.

---

## Relación con las fases anteriores

- **Fase 1:** diagnóstico y auditoría inicial.
- **Fase 2:** limpieza, transformación y validación funcional.
- **Fase 3:** POO, recursividad y medición de eficiencia.
- **Fase 4:** visualización, interpretación y comunicación de resultados.

---

## Trazabilidad de cambios

Los cambios del notebook y `utils.py` se registran en:

```text
../changelog.md
```

---

## Salidas esperadas

- Notebook ejecutado sin errores.
- Dataset procesado y validado.
- Visualizaciones analíticas.
- Interpretaciones y conclusiones.
- Informe técnico de Fase 4.
- `changelog.md` actualizado.
- Repositorio con trazabilidad.

---

## Licencia

La licencia general del proyecto se encuentra en el archivo `LICENSE` ubicado en la raíz del repositorio.
