# MCDIA500 - Programación para Ciencia de Datos

## Objetivo del proyecto

Este proyecto tiene como objetivo desarrollar un flujo de trabajo reproducible para el análisis de un dataset de diabetes, aplicando técnicas de programación en Python orientadas a ciencia de datos.

El trabajo considera la carga, exploración, limpieza y preparación de datos con presencia de registros sucios, valores inválidos, datos faltantes y formatos inconsistentes. Posteriormente, el proyecto busca construir una base experimental que permita aplicar modelos de machine learning para predecir la variable `Outcome`, asociada a la presencia o ausencia de diabetes.

El proyecto está organizado para facilitar la trazabilidad, reutilización de funciones, ejecución en notebooks de Jupyter y control de versiones mediante GitHub.

---

## Estructura del proyecto

## Estructura del proyecto

```text
mcdia500-programacion-cd-g6/
│
├── data/
│   ├── raw/
│   │   └── diabetes_raw.csv
│   │
│   └── processed/
│       └── .gitkeep
│
├── docs/
│   └── .gitkeep
│
├── notebooks/
│   └── 
│
├── reports/
│   └── .gitkeep
│
├── src/
│   └── utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Descripción de carpetas

- `data/raw/`: contiene los datos originales o crudos del proyecto.
- `data/processed/`: contiene datasets procesados, limpios o transformados.
- `docs/`: contiene documentación complementaria del proyecto.
- `notebooks/`: contiene los notebooks de análisis, limpieza, experimentación y modelamiento.
- `reports/`: contiene reportes, resultados, gráficos exportados o conclusiones generadas.
- `src/`: contiene funciones reutilizables, módulos auxiliares y código Python del proyecto.

---

## Requisitos previos

Antes de ejecutar el proyecto, se requiere tener instalado:

- Python 3.12.x
- Git
- Visual Studio Code, JupyterLab o Jupyter Notebook

---

## Instalación del proyecto

### 1. Clonar el repositorio

```powershell
git clone https://github.com/MagUnab/mcdia500-programacion-cd-g6.git
```

Ingresar a la carpeta del proyecto:

```powershell
cd mcdia500-programacion-cd-g6
```

---

### 2. Crear el entorno virtual

```powershell
python -m venv .venv
```

---

### 3. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Si la activación fue correcta, se debe ver algo como esto:

```text
(.venv) PS C:\ruta\del\proyecto>
```

---

### 4. Actualizar pip

```powershell
python -m pip install --upgrade pip
```

---

### 5. Instalar las dependencias del proyecto

```powershell
python -m pip install -r requirements.txt
```

---

### 6. Registrar el entorno virtual como kernel de Jupyter

```powershell
python -m ipykernel install --user --name mcdia500-g6 --display-name "Python 3.12 - MCDIA500 G6"
```

---

### 7. Ejecutar JupyterLab

```powershell
jupyter lab
```

Dentro de JupyterLab seleccionarel kernel:

```text
Kernel → Change Kernel → Python 3.12 - MCDIA500 G6
```

---

## Uso del proyecto

Los notebooks del proyecto se encuentran en la carpeta:

```text
notebooks/
```

Los datos originales se encuentran en:

```text
raw/
```

Las funciones reutilizables se encuentran en:

```text
src/
```

Desde un notebook ubicado en la carpeta `notebooks/`, se pueden importar funciones desde `src/` usando:

```python
import sys
from pathlib import Path

project_root = Path.cwd().parent
sys.path.append(str(project_root / "src"))
```

Ejemplo de carga de datos:

```python
import pandas as pd

df = pd.read_csv("../raw/diabetes_raw.csv", sep=";")
df.head()
```

---

## Control de versiones

Para revisar el estado del repositorio:

```powershell
git status
```

Para agregar cambios:

```powershell
git add .
```

Para crear un commit:

```powershell
git commit -m "Actualizar avance del proyecto"
```

Para subir los cambios a GitHub:

```powershell
git push
```

---

## Archivos que no deben subirse al repositorio

La carpeta `.venv/` no debe subirse a GitHub, ya que cada persona que quiera clonar y trabajar en este proyecto debe crear su propio entorno virtual local a partir del archivo `requirements.txt`.

El archivo `.gitignore` debería considerar al menos:

```gitignore
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
.env
```

---

## Reproducibilidad

Para reproducir el proyecto en otro equipo, se deben ejecutar los siguientes pasos:

```powershell
git clone https://github.com/MagUnab/mcdia500-programacion-cd-g6.git
cd mcdia500-programacion-cd-g6
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name mcdia500-g6 --display-name "Python 3.12 - MCDIA500 G6"
python -m jupyterlab --ServerApp.use_redirect_file=False
```

Con estos pasos, el entorno queda configurado para ejecutar los notebooks del proyecto.