"""
utils.py — Funciones reutilizables del pipeline de preprocesamiento
Proyecto : Análisis y Predicción de Diabetes
Curso    : MCDI500 — Herramientas de Software Científico
Fase     : 2 — Obtención, Limpieza y Transformación de Datos

Este módulo centraliza todas las funciones del pipeline de datos.
Se importa al inicio del notebook para que las funciones estén
disponibles desde cualquier celda, haciéndolas verdaderamente
reutilizables e independientes del orden de ejecución.

Uso en el notebook:
    import sys, os
    sys.path.insert(0, os.path.abspath('..'))
    from src.utils import *
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler


def cargar_datos(ruta: Path) -> pd.DataFrame:
    """
    Lee el dataset crudo desde la ruta indicada y devuelve un DataFrame.

    Parámetros
    ----------
    ruta : Path
        Ruta al archivo CSV con separador ';'.

    Retorna
    -------
    pd.DataFrame
        Dataset crudo sin modificar.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe en la ruta indicada.
    ValueError
        Si el DataFrame resultante está vacío.
    """
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    df = pd.read_csv(ruta, sep=";")
    if df.empty:
        raise ValueError(f"El dataset está vacío: {ruta}")
    return df




def explorar_dataset(df: pd.DataFrame) -> None:
    """
    Diagnóstico completo del DataFrame.

    Imprime: tipos de datos, información general, valores nulos,
    ceros en columnas clínicas, outliers extremos, duplicados,
    estadísticos descriptivos y balance de la variable objetivo.

    Parámetros
    ----------
    df : pd.DataFrame
        Dataset a diagnosticar.
    """
    SEP = "=" * 60

    print(f"{SEP}\n[1] TIPOS DE DATOS\n{SEP}")
    print(df.dtypes.to_string())

    print(f"\n{SEP}\n[2] INFORMACIÓN GENERAL\n{SEP}")
    df.info()

    print(f"\n{SEP}\n[3] VALORES NULOS POR COLUMNA\n{SEP}")
    nulos = df.isna().sum()
    pct   = (nulos / len(df) * 100).round(2)
    print(pd.DataFrame({'Nulos': nulos, 'Porcentaje (%)': pct}).to_string())

    print(f"\n{SEP}\n[4] CEROS EN COLUMNAS CLÍNICAS (biológicamente imposibles)\n{SEP}")
    cols_clinicas = ['Glucose', 'BloodPressure', 'BMI', 'SkinThickness', 'Insulin']
    for col in cols_clinicas:
        if col in df.columns:
            n = (pd.to_numeric(df[col], errors='coerce') == 0).sum()
            print(f"  {col:<30}: {n} ceros")

    print(f"\n{SEP}\n[5] VALORES CENTINELA Y OUTLIERS EXTREMOS\n{SEP}")
    print(f"  Glucose  > 300  : {(df['Glucose'] > 300).sum()} filas (centinela 999)")
    print(f"  Age      > 100  : {(df['Age'] > 100).sum()} filas (centinela 150)")
    print(f"  BMI      > 60   : {(df['BMI'] > 60).sum()} filas")
    n_interrogante = (df['BloodPressure'].astype(str) == '?').sum()
    n_unidad = df['BloodPressure'].astype(str).str.contains('mmHg', na=False).sum()
    print(f"  BloodPressure '?'   : {n_interrogante} filas")
    print(f"  BloodPressure 'mmHg': {n_unidad} filas con unidad embebida")

    print(f"\n{SEP}\n[6] FILAS DUPLICADAS\n{SEP}")
    print(f"  Total duplicadas: {df.duplicated().sum()}")

    print(f"\n{SEP}\n[7] ESTADÍSTICOS DESCRIPTIVOS\n{SEP}")
    print(df.describe().round(3).to_string())

    print(f"\n{SEP}\n[8] DISTRIBUCIÓN VARIABLE OBJETIVO (Outcome)\n{SEP}")
    conteo = df['Outcome'].value_counts()
    pct_o  = df['Outcome'].value_counts(normalize=True).mul(100).round(2)
    print(pd.DataFrame({'Conteo': conteo, '%': pct_o}).to_string())


# Alias para compatibilidad con el nombre del original


def eliminar_columnas(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Elimina columnas con calidad insuficiente del DataFrame.

    Se elimina SkinThickness porque el 32.6% de sus registros
    son no confiables (504 ceros + 164 NaN), lo que hace inviable
    cualquier estrategia de imputación sin introducir sesgo.

    Parámetros
    ----------
    df      : pd.DataFrame
    columnas: list  columnas a eliminar.

    Retorna
    -------
    pd.DataFrame  sin las columnas eliminadas.
    """
    df = df.copy()
    df = df.drop(columns=columnas)
    print(f"[COLUMNAS ELIMINADAS] {columnas}")
    print(f"  Columnas restantes: {list(df.columns)}")
    return df


def castear_bloodpressure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y convierte la columna BloodPressure de str a float.

    Problemas tratados:
      - Valores con unidad 'mmHg' embebida: se extrae el número
        con str.replace(r'\\s*mmHg', '', regex=True).
      - Valores '?': pd.to_numeric(errors='coerce') los convierte a NaN.
      - Resto: cadenas numéricas válidas convertidas a float.

    Parámetros
    ----------
    df : pd.DataFrame  (BloodPressure como str)

    Retorna
    -------
    pd.DataFrame  con BloodPressure como float64.
    """
    df = df.copy()
    # Paso 1: eliminar la unidad 'mmHg'
    df['BloodPressure'] = (
        df['BloodPressure']
        .astype(str)
        .str.replace(r'\s*mmHg', '', regex=True)
        .str.strip()
    )
    # Paso 2: convertir a numérico — '?' y residuos → NaN
    df['BloodPressure'] = pd.to_numeric(df['BloodPressure'], errors='coerce')
    print("[CASTING BloodPressure]")
    print(f"  Tipo resultante : {df['BloodPressure'].dtype}")
    print(f"  NaN en BP       : {df['BloodPressure'].isna().sum()}  (de '?' y valores no numéricos)")
    return df


def reemplazar_invalidos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reemplaza ceros biológicamente imposibles y valores centinela por NaN.

    Ceros imposibles: Glucose, BloodPressure, Insulin y BMI no pueden
    ser cero en una persona viva; codifican datos faltantes.

    Valores centinela:
      - Glucose = 999  → imposible clínicamente (máx. fisiológico ~400 mg/dL).
      - Age = 150      → imposible biológicamente.
      - BMI > 60       → probable error de digitación.

    Parámetros
    ----------
    df : pd.DataFrame  (con BloodPressure ya como float)

    Retorna
    -------
    pd.DataFrame  con inválidos convertidos a NaN.
    """
    df = df.copy()
    cols_ceros = ['Glucose', 'BloodPressure', 'BMI', 'Insulin']
    print("[CEROS IMPOSIBLES → NaN]")
    for col in cols_ceros:
        if col in df.columns:
            n = (df[col] == 0).sum()
            df[col] = df[col].replace(0, np.nan)
            print(f"  {col:<20}: {n:4d} ceros reemplazados")

    print("\n[VALORES CENTINELA / OUTLIERS EXTREMOS → NaN]")
    n_g = (df['Glucose'] > 300).sum()
    df['Glucose'] = df['Glucose'].where(df['Glucose'] <= 300, np.nan)
    print(f"  Glucose > 300             : {n_g:4d} → NaN")

    n_a = (df['Age'] > 100).sum()
    df['Age'] = df['Age'].where(df['Age'] <= 100, np.nan)
    print(f"  Age > 100 (centinela 150) : {n_a:4d} → NaN")

    n_b_alto = (df['BMI'] > 60).sum()
    n_b_bajo = ((df['BMI'] < 10) & (df['BMI'] > 0)).sum()
    df['BMI'] = df['BMI'].where(df['BMI'] <= 60, np.nan)
    df['BMI'] = df['BMI'].where((df['BMI'] >= 10) | (df['BMI'].isna()), np.nan)
    print(f"  BMI > 60                  : {n_b_alto:4d} → NaN")
    print(f"  BMI < 10 (error digitación): {n_b_bajo:4d} → NaN")

    print(f"\n  NaN totales tras este paso: {df.isna().sum().sum()}")
    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas exactamente duplicadas conservando la primera ocurrencia.

    Los duplicados pueden provenir de errores en la recolección o de la
    unión de múltiples fuentes. Mantenerlos inflaría artificialmente
    las métricas del modelo y la representatividad estadística.

    Parámetros
    ----------
    df : pd.DataFrame

    Retorna
    -------
    pd.DataFrame  sin filas duplicadas, con índice reiniciado.
    """
    n_antes = len(df)
    df = df.drop_duplicates(keep='first').reset_index(drop=True)
    n_elim = n_antes - len(df)
    print(f"[DUPLICADOS]  Antes: {n_antes} | Eliminadas: {n_elim} | Después: {len(df)}")
    return df


# ── Ejecutar pipeline de limpieza ────────────────────────────


def imputar_mediana(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Imputa valores NaN con la mediana de cada columna especificada.

    La mediana se calcula sobre los datos válidos del DataFrame de entrada,
    es decir, post-reemplazo de ceros y outliers extremos. Esto garantiza
    que el valor imputado refleje la distribución real de datos válidos.

    Parámetros
    ----------
    df      : pd.DataFrame
    columnas: list  columnas a imputar.

    Retorna
    -------
    pd.DataFrame  sin NaN en las columnas indicadas.
    """
    df = df.copy()
    print("[IMPUTACIÓN POR MEDIANA]")
    for col in columnas:
        if col not in df.columns:
            continue
        n   = df[col].isna().sum()
        med = df[col].median()
        df[col] = df[col].fillna(med)
        estado = f"{n:4d} NaN → mediana = {med:.3f}" if n > 0 else "sin NaN"
        print(f"  {col:<28}: {estado}")
    print(f"\n  NaN restantes en el dataset: {df.isna().sum().sum()}")
    return df




def validar_post_limpieza(df: pd.DataFrame) -> None:
    """
    Verifica la calidad del dataset tras limpieza e imputación.

    Incluye asserts de rangos biológicos que DEBEN ejecutarse
    ANTES del escalamiento, ya que StandardScaler modifica los
    valores numéricos al transformarlos a Z-score.

    Parámetros
    ----------
    df : pd.DataFrame  dataset post-limpieza, pre-escalamiento.
    """
    print('REVISIÓN COLUMNA POR COLUMNA')
    for col in df.columns:
        print(f"\n{'='*50}")
        print(f'Columna       : {col}')
        print(f'Tipo          : {df[col].dtype}')
        print(f'Nulos         : {df[col].isnull().sum()}')
        print(f'Valores únicos: {df[col].nunique()}')

    print(f"\n{'='*50}")
    total_nulos = df.isna().sum().sum()
    print(f'NaN totales restantes: {total_nulos}')
    if total_nulos == 0:
        print('✓ Sin valores faltantes — dataset listo para transformaciones.')

    # ── Asserts de rangos biológicos (ANTES del escalamiento) ──
    print(f"\n{'='*50}")
    print('ASSERTS DE RANGOS BIOLÓGICOS (pre-escalamiento):')

    assert df['Age'].between(0, 100).all(), \
        'Age fuera del rango válido [0, 100]'
    print('✓ Age en rango válido [0, 100]')

    assert (df['Glucose'] > 0).all(), \
        'Hay valores de Glucose ≤ 0 — imputación incompleta'
    print('✓ Glucose > 0 en todas las filas')

    assert (df['BloodPressure'] > 0).all(), \
        'Hay valores de BloodPressure ≤ 0 — imputación incompleta'
    print('✓ BloodPressure > 0 en todas las filas')

    assert (df['BMI'] > 0).all() and (df['BMI'] <= 60).all(), \
        f'BMI fuera del rango válido (0, 60]: min={df["BMI"].min():.2f}'
    print(f'✓ BMI en rango válido (0, 60]: min={df["BMI"].min():.2f}, max={df["BMI"].max():.2f}')

    assert df.duplicated().sum() == 0, \
        'Hay filas duplicadas'
    print('✓ Sin filas duplicadas')

    assert df.isna().sum().sum() == 0, \
        'Quedan valores NaN'
    print('✓ Sin NaN en el dataset')

    print(f"\n{'='*50}")
    print('✅ Todas las validaciones pre-escalamiento pasaron')




def analizar_rangos(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Cuantifica valores <= 0 en las columnas numéricas indicadas.

    Permite verificar que no quedan valores incoherentes con el
    dominio clínico del problema tras la limpieza.

    Parámetros
    ----------
    df      : pd.DataFrame
    columnas: list  columnas numéricas a evaluar.

    Retorna
    -------
    pd.DataFrame  con columnas Variable, Valores<=0, Porcentaje(%).
    """
    resumen = pd.DataFrame({
        'Variable':       columnas,
        'Valores <= 0':   [(df[c] <= 0).sum() for c in columnas],
        'Porcentaje (%)': [round((df[c] <= 0).sum() / len(df) * 100, 2) for c in columnas],
    })
    return resumen.sort_values('Porcentaje (%)', ascending=False).reset_index(drop=True)


def detectar_outliers_iqr(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Detecta outliers estadísticos usando el método IQR.

    Un valor es outlier si está fuera de [Q1 - 1.5·IQR, Q3 + 1.5·IQR].
    Los outliers detectados NO se eliminan automáticamente: en datos
    clínicos pueden representar condiciones reales de algunos pacientes
    y requieren interpretación contextual antes de cualquier decisión.

    Parámetros
    ----------
    df      : pd.DataFrame
    columnas: list  columnas numéricas a evaluar.

    Retorna
    -------
    pd.DataFrame  con Variable y Cantidad de Outliers.
    """
    resultado = []
    for col in columnas:
        q1  = df[col].quantile(0.25)
        q3  = df[col].quantile(0.75)
        iqr = q3 - q1
        li  = q1 - 1.5 * iqr
        ls  = q3 + 1.5 * iqr
        n   = ((df[col] < li) | (df[col] > ls)).sum()
        resultado.append([col, n])
    return pd.DataFrame(resultado, columns=['Variable', 'Cantidad de Outliers']) \
             .sort_values('Cantidad de Outliers', ascending=False).reset_index(drop=True)




def crear_variables_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera variables categóricas derivadas a partir de Age y BMI.

    AgeGroup: segmenta la edad en rangos clínicos estándar
      (18-29 | 30-44 | 45-59 | 60+).
    BMI_Category: clasifica el IMC según criterios OMS
      (Bajo_peso < 18.5 | Normal 18.5-25 | Sobrepeso 25-30 | Obesidad > 30).

    Parámetros
    ----------
    df : pd.DataFrame

    Retorna
    -------
    pd.DataFrame  con AgeGroup y BMI_Category añadidas.
    """
    df = df.copy()

    # AgeGroup
    df['AgeGroup'] = pd.cut(
        df['Age'],
        bins=[0, 29, 44, 59, 200],
        labels=['18-29', '30-44', '45-59', '60+'],
        right=True
    )

    # BMI_Category (OMS)
    df['BMI_Category'] = pd.cut(
        df['BMI'],
        bins=[0, 18.5, 25.0, 30.0, 200],
        labels=['Bajo_peso', 'Normal', 'Sobrepeso', 'Obesidad'],
        right=True
    )

    print("[VARIABLES DERIVADAS]")
    print("  AgeGroup:\n",    df['AgeGroup'].value_counts().sort_index().to_string())
    print("  BMI_Category:\n", df['BMI_Category'].value_counts().sort_index().to_string())
    return df




def codificar_categoricas(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Aplica One-Hot Encoding a las variables categóricas indicadas.

    Se usa pd.get_dummies con drop_first=True para evitar la trampa de la
    variable dummy (multicolinealidad perfecta en modelos lineales).

    Parámetros
    ----------
    df      : pd.DataFrame
    columnas: list   variables categóricas a codificar.

    Retorna
    -------
    pd.DataFrame  con dummies binarias añadidas.
    """
    df = df.copy()
    print('[ONE-HOT ENCODING]')
    for col in columnas:
        n_antes = df.shape[1]
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True, dtype=int)
        df = pd.concat([df, dummies], axis=1)
        cols_nuevas = list(dummies.columns)
        print(f'  {col} → {cols_nuevas} ({len(cols_nuevas)} columnas nuevas)')
    print(f'\n  Columnas antes: {n_antes} | Columnas después: {df.shape[1]}')
    return df




def escalar_variables(df: pd.DataFrame, columnas: list) -> pd.DataFrame:
    """
    Aplica estandarización Z-score (StandardScaler) a las columnas indicadas.

    Transforma cada variable para que tenga media=0 y std=1.
    Se conservan las columnas originales; las escaladas reemplazan
    sus valores en las mismas columnas para mantener el dataset compacto.

    Se elige StandardScaler sobre MinMaxScaler porque las distribuciones
    clínicas son asimétricas con outliers residuales: Z-score es más
    robusto en este contexto y es requerido por SVM, regresión logística
    y PCA.

    Parámetros
    ----------
    df      : pd.DataFrame
    columnas: list  columnas numéricas a escalar.

    Retorna
    -------
    pd.DataFrame  con las columnas escaladas in-place.
    """
    df = df.copy()
    scaler = StandardScaler()
    df[columnas] = scaler.fit_transform(df[columnas])

    print("[ESCALAMIENTO StandardScaler]")
    print(f"  Columnas escaladas: {columnas}")
    print("\n  Verificación — media y desviación estándar post-escalamiento:")
    print(f"  (media ≈ 0 y std ≈ 1 confirman aplicación correcta)")
    return df




def validar_dataset_final(df_original: pd.DataFrame,
                           df_final:    pd.DataFrame) -> None:
    """
    Validación técnica completa del dataset procesado.

    Verifica mediante assert (casos normales, límite y excepciones):
      1. Sin NaN en columnas numéricas base.
      2. Sin filas duplicadas.
      3. Variable objetivo solo contiene {0, 1}.
      4. Coherencia dimensional (no más filas que el original).
      5. Columnas escaladas tienen media ≈ 0 y std ≈ 1.
      6. Outcome no fue escalado (conserva valores binarios).

    NOTA: Los rangos biológicos (Age, Glucose, BloodPressure, BMI)
    se verifican ANTES del escalamiento en validar_post_limpieza(),
    ya que StandardScaler modifica los rangos numéricos al transformar
    los datos a Z-score (media=0, std=1).

    Parámetros
    ----------
    df_original : pd.DataFrame  dataset crudo (referencia de tamaño).
    df_final    : pd.DataFrame  dataset procesado a validar.

    Raises
    ------
    AssertionError  si alguna verificación falla.
    """
    COLS_BASE = ['Pregnancies', 'Glucose', 'BloodPressure',
                 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
                 'Age', 'Outcome']
    COLS_ESCALADAS = ['Pregnancies', 'Glucose', 'BloodPressure',
                      'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

    print('=' * 55)
    print('VALIDACIÓN TÉCNICA FINAL')
    print('=' * 55)

    # 1 — Sin NaN en columnas base
    n_nan = df_final[COLS_BASE].isna().sum().sum()
    assert n_nan == 0, f'Quedan {n_nan} NaN en columnas base'
    print('✓ Sin NaN en columnas numéricas base')

    # 2 — Sin duplicados
    n_dup = df_final.duplicated().sum()
    assert n_dup == 0, f'Hay {n_dup} filas duplicadas'
    print('✓ Sin filas duplicadas')

    # 3 — Outcome en {0, 1}
    vals = set(df_final['Outcome'].unique())
    assert vals.issubset({0, 1}), f'Outcome contiene valores inesperados: {vals}'
    print('✓ Outcome solo contiene {0, 1}')

    # 4 — Coherencia dimensional
    assert len(df_final) <= len(df_original), \
        'El dataset final tiene más filas que el original'
    diff = len(df_original) - len(df_final)
    print(f'✓ Coherencia dimensional: {len(df_original)} → {len(df_final)} ({diff} filas eliminadas)')

    # 5 — Columnas escaladas: media ≈ 0 y std ≈ 1
    # (los rangos biológicos se verifican antes del escalamiento
    #  en validar_post_limpieza(), ya que StandardScaler modifica
    #  los valores numéricos al transformarlos a Z-score)
    for col in COLS_ESCALADAS:
        media = df_final[col].mean()
        std   = df_final[col].std()
        assert abs(media) < 1e-6, f'{col}: media = {media:.6f} (esperado ≈ 0)'
        assert abs(std - 1) < 0.01, f'{col}: std = {std:.6f} (esperado ≈ 1)'
    print(f'✓ {len(COLS_ESCALADAS)} columnas escaladas con media≈0 y std≈1')

    # 6 — Outcome no escalado
    assert df_final['Outcome'].isin([0, 1]).all(), \
        'Outcome parece haber sido escalado por error'
    print('✓ Outcome conserva valores binarios {0, 1} (no fue escalado)')

    # df.info() — evidencia visible del dataset final
    print(f'\n{"-" * 55}')
    print('INFORMACIÓN DEL DATASET FINAL (df.info()):')
    print(f'{"-" * 55}')
    df_final.info()

    print('\n' + '=' * 55)
    print('✅  TODAS LAS VALIDACIONES PASARON EXITOSAMENTE')
    print('=' * 55)




def resumen_comparativo(df_raw:   pd.DataFrame,
                         df_final: pd.DataFrame) -> None:
    """
    Muestra métricas clave del dataset antes y después del pipeline.

    Parámetros
    ----------
    df_raw   : pd.DataFrame  dataset crudo original.
    df_final : pd.DataFrame  dataset procesado.
    """
    COLS_BASE = ['Pregnancies', 'Glucose', 'BloodPressure',
                 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
                 'Age', 'Outcome']

    resumen = pd.DataFrame({
        'Métrica': ['Filas', 'Columnas', 'NaN totales', 'Duplicados',
                    'Tipo BloodPressure'],
        'RAW (original)': [
            df_raw.shape[0],
            df_raw.shape[1],
            df_raw.isna().sum().sum(),
            df_raw.duplicated().sum(),
            str(df_raw['BloodPressure'].dtype),
        ],
        'Procesado (final)': [
            df_final.shape[0],
            df_final.shape[1],
            df_final[COLS_BASE].isna().sum().sum(),
            df_final.duplicated().sum(),
            str(df_final['BloodPressure'].dtype),
        ],
    })

    print("=" * 60)
    print("COMPARACIÓN RAW vs PROCESADO")
    print("=" * 60)
    print(resumen.to_string(index=False))

    print("\nDistribución final de Outcome:")
    conteo = df_final['Outcome'].value_counts()
    pct    = df_final['Outcome'].value_counts(normalize=True).mul(100).round(2)
    print(pd.DataFrame({'Conteo': conteo, '%': pct}).to_string())




def exportar_dataset(df: pd.DataFrame, ruta: Path) -> None:
    """
    Exporta el dataset procesado a CSV y verifica la escritura.

    Se usa separador ',' (estándar internacional) y se omite el
    índice de fila para mantener el archivo limpio. Tras guardar,
    se relée el archivo para confirmar que las dimensiones coinciden.

    Parámetros
    ----------
    df   : pd.DataFrame  dataset final.
    ruta : Path          ruta de destino.
    """
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False, encoding='utf-8')

    print("=" * 55)
    print("EXPORTACIÓN COMPLETADA")
    print("=" * 55)
    print(f"  Archivo   : {ruta}")
    print(f"  Filas     : {df.shape[0]}")
    print(f"  Columnas  : {df.shape[1]}")
    print(f"  Tamaño    : {ruta.stat().st_size / 1024:.1f} KB")

    df_check = pd.read_csv(ruta)
    assert df_check.shape == df.shape, \
        f"Dimensiones al releer ({df_check.shape}) ≠ DataFrame ({df.shape})"
    print(f"\n✓ Verificación: {df_check.shape[0]} filas × {df_check.shape[1]} cols — coincide.")

    print("\nColumnas del dataset exportado:")
    for col in df.columns:
        print(f"  - {col:<28} [{df[col].dtype}]")




