# Fase 1 - Diagnóstico y Auditoría Inicial de Calidad de Datos Clínicos

Este directorio contiene el desarrollo correspondiente a la **Fase 1** del proyecto del curso **MCDIA500 - Programación para la Ciencia de Datos**.

El propósito de esta fase es establecer una base técnica reproducible para la carga, inspección y auditoría inicial del dataset clínico `diabetes_raw.csv`, sin modificar el archivo original. La Fase 1 se limita a diagnosticar la estructura inicial del conjunto de datos, verificar el entorno computacional y documentar un flujo mínimo de trabajo reproducible.

> **Importante:** En esta fase no se realiza limpieza, imputación, transformación, partición de datos, entrenamiento de modelos ni evaluación predictiva. Estas actividades quedan proyectadas para fases posteriores del proyecto.

---

## Objetivo de la Fase 1

Desarrollar un flujo secuencial interactivo de auditoría y diagnóstico estructural de datos en Python para caracterizar de manera reproducible el estado inicial del conjunto de datos clínicos `diabetes_raw.csv`, verificando dimensiones, columnas, tipos de datos, valores faltantes, registros duplicados y distribución de la variable objetivo, sin modificar el archivo original durante la Fase 1 del proyecto.

---

## Alcance de esta fase

La Fase 1 considera las siguientes actividades:

* Configuración de un entorno reproducible de trabajo.
* Declaración de dependencias mediante `requirements.txt`.
* Carga del archivo crudo `diabetes_raw.csv` desde una ruta relativa.
* Inspección inicial de dimensiones, columnas y tipos de datos.
* Diagnóstico básico de valores faltantes.
* Identificación de registros duplicados exactos.
* Revisión de la distribución de la variable objetivo `Outcome`.
* Documentación inicial del flujo de trabajo en un notebook Jupyter.
* Organización del repositorio según una estructura reproducible.

Quedan fuera del alcance de esta fase:

* Limpieza del dataset.
* Conversión o saneamiento de variables.
* Imputación de valores faltantes.
* Eliminación de duplicados.
* Normalización o escalamiento de variables.
* Generación de datasets procesados.
* Análisis exploratorio profundo.
* Partición `train/test`.
* Entrenamiento de modelos de machine learning.
* Evaluación mediante métricas predictivas.

---

## Estructura de la carpeta F1

```text
F1/
├── data/
│   ├── raw/
│   │   └── diabetes_raw.csv
│   └── processed/
│       └── .gitkeep
├── docs/
├── notebooks/
│   └── F1_Definicion.ipynb
├── reports/
│   └── .gitkeep
├── src/
│   └── .gitkeep
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Descripción de carpetas y archivos

| Elemento           | Descripción                                                                                                      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `data/raw/`        | Contiene el dataset original `diabetes_raw.csv`. Este archivo no debe modificarse.                               |
| `data/processed/`  | Carpeta reservada para datasets procesados que serán generados en fases posteriores.                             |
| `docs/`            | Contiene documentos formales asociados a la entrega de Fase 1.                                                   |
| `notebooks/`       | Contiene el notebook `F1_Definicion.ipynb`, utilizado para la carga inicial y auditoría estructural básica.      |
| `reports/`         | Carpeta reservada para salidas, figuras o reportes que serán generados en fases posteriores.                     |
| `src/`             | Carpeta reservada para funciones reutilizables y módulos auxiliares que serán incorporados en fases posteriores. |
| `requirements.txt` | Declara las dependencias necesarias para ejecutar el notebook de Fase 1.                                         |
| `README.md`        | Documento de orientación técnica para reproducir la Fase 1.                                                      |
| `.gitignore`       | Define archivos y carpetas excluidos del control de versiones.                                                   |
| `LICENSE`          | Archivo de licencia del proyecto.                                                                                |

---

## Entorno de ejecución

El notebook fue ejecutado y verificado con el siguiente entorno:

```text
Python 3.12.4
NumPy 1.26.4
Pandas 2.2.2
ipykernel 6.28.0
notebook 7.0.8
JupyterLab 4.0.11
```

Estas versiones se encuentran declaradas en el archivo `requirements.txt` de la Fase 1.

---

## Dependencias principales

El archivo `requirements.txt` contiene las dependencias necesarias para ejecutar el notebook de Fase 1:

```text
jupyterlab==4.0.11
notebook==7.0.8
ipykernel==6.28.0
pandas==2.2.2
numpy==1.26.4
```

No se incorporan librerías de modelamiento predictivo, visualización avanzada ni aprendizaje automático, ya que no forman parte del alcance operativo de esta fase.

---

## Instrucciones de reproducción

### 1. Clonar el repositorio

```bash
git clone https://github.com/edocontreras/mcdia500-programacion-cd-g6.git
```

### 2. Ingresar a la carpeta de la Fase 1

```bash
cd mcdia500-programacion-cd-g6/F1
```

### 3. Crear un entorno virtual

En Windows:

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

En Windows CMD:

```bash
.venv\Scripts\activate.bat
```

### 5. Actualizar `pip`

```bash
python -m pip install --upgrade pip
```

### 6. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 7. Registrar el kernel de Jupyter

```bash
python -m ipykernel install --user --name mcdia500-f1-g6 --display-name "Python 3.12.4 - MCDIA500 F1 G6"
```

### 8. Abrir JupyterLab

```bash
python -m jupyterlab
```

### 9. Ejecutar el notebook

Abrir el archivo:

```text
notebooks/F1_Definicion.ipynb
```

Luego seleccionar el kernel:

```text
Python 3.12.4 - MCDIA500 F1 G6
```

Finalmente, ejecutar:

```text
Kernel > Restart Kernel and Run All Cells
```

La ejecución se considera correcta si el notebook finaliza sin errores y muestra la verificación del entorno, la carga del dataset, las dimensiones, columnas, tipos de datos, valores faltantes, duplicados exactos y distribución de `Outcome`.

---

## Notebook principal

El notebook principal de esta fase es:

```text
notebooks/F1_Definicion.ipynb
```

Este notebook realiza las siguientes acciones:

* Verifica las versiones del entorno de ejecución.
* Carga el archivo `diabetes_raw.csv` desde `data/raw/`.
* Revisa la existencia de la ruta relativa del dataset.
* Muestra dimensiones del conjunto de datos.
* Lista columnas disponibles.
* Inspecciona tipos de datos.
* Ejecuta `df.info()`.
* Muestra las primeras filas del dataset.
* Reporta valores nulos por variable.
* Reporta duplicados exactos.
* Calcula la distribución absoluta y porcentual de la variable objetivo `Outcome`.

---

## Dataset utilizado

El archivo de datos utilizado en esta fase es:

```text
data/raw/diabetes_raw.csv
```

Este archivo se mantiene en estado crudo y no debe sobrescribirse ni modificarse durante la Fase 1. Toda acción realizada en el notebook corresponde a lectura, inspección y diagnóstico inicial.

---

## Control de versiones

El proyecto utiliza Git y GitHub para mantener trazabilidad del avance técnico. Se recomienda utilizar mensajes de commit descriptivos, siguiendo una convención simple basada en prefijos.

Ejemplos de prefijos:

| Prefijo   | Uso                                            |
| --------- | ---------------------------------------------- |
| `docs:`   | Cambios en documentación o README.             |
| `fix:`    | Corrección de errores o ajustes de coherencia. |
| `config:` | Ajustes de dependencias o configuración.       |
| `data:`   | Incorporación o movimiento de datos.           |
| `chore:`  | Cambios de estructura o mantenimiento.         |

Ejemplo de commit recomendado para esta fase:

```bash
git add F1/README.md F1/requirements.txt F1/notebooks/F1_Definicion.ipynb
git commit -m "fix: corrige coherencia técnica de Fase 1 según rúbrica"
git push
```

---

## Estado de componentes de Fase 1

| Componente                                 | Estado                            |
| ------------------------------------------ | --------------------------------- |
| Dataset crudo en `data/raw/`               | Implementado                      |
| Carpeta `data/processed/`                  | Proyectada para fases posteriores |
| Notebook de definición y auditoría inicial | Implementado                      |
| Archivo `requirements.txt`                 | Implementado                      |
| Carpeta `src/`                             | Proyectada para fases posteriores |
| Carpeta `reports/`                         | Proyectada para fases posteriores |
| Limpieza de datos                          | Fuera del alcance de Fase 1       |
| Modelamiento predictivo                    | Fuera del alcance de Fase 1       |
| Evaluación de métricas predictivas         | Fuera del alcance de Fase 1       |

---

## Integrantes

* Gonzalo Bouldres V.
* Luis Díaz G.
* Eduardo Contreras C.

---

## Observación final

Esta carpeta constituye la base reproducible de la Fase 1. Su propósito es documentar y ejecutar una auditoría inicial del dataset clínico sin alterar la fuente original. Los resultados obtenidos permiten establecer una línea base técnica para las fases posteriores del proyecto, donde se abordarán limpieza, transformación, análisis exploratorio, modelamiento y evaluación.
