# ==============================================================================
# ARCHIVO: src/utils.py
# PROYECTO: Pipeline de Saneamiento y Preparación Clínica - Fase 3 (POO)
# CURSO: MCDI500 — Programación para la Ciencia de Datos (UNAB)
# ==============================================================================

import os
import re
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler

# ==============================================================================
# 1. COMPONENTE RECURSIVO DE INFRAESTRUCTURA (Exigencia Algorítmica)
# ==============================================================================

def auditar_carpetas_recursivo(ruta_actual: str, profundidad: int = 0):
    """
    Recorre de forma recursiva los directorios del proyecto para listar la 
    estructura jerárquica y verificar la existencia de los activos de datos.
    """
    try:
        for item in os.listdir(ruta_actual):
            ruta_completa = os.path.join(ruta_actual, item)
            if any(omitir in ruta_completa for omitir in [".git", "__pycache__", ".venv"]):
                continue
                
            if os.path.isdir(ruta_completa):
                print("  " * profundidad + f" [{item}]")
                auditar_carpetas_recursivo(ruta_completa, profundidad + 1)
            elif item.endswith(('.csv', '.ipynb', '.py')):
                print("  " * profundidad + f" {item}")
    except Exception as e:
        print(f"Error en auditoría recursiva: {e}")


# ==============================================================================
# 2. CLASE PRINCIPAL: PIPELINE DE PREPROCESAMIENTO (POO & Encapsulamiento)
# ==============================================================================

class PreprocesadorDiabetes:
    """
    Clase que centraliza y encapsula el pipeline de datos clínicos de diabetes.
    Mantiene el estado interno de la matriz mediante atributos de instancia,
    evitando variables volátiles sueltas en el Kernel del notebook.
    """
    def __init__(self, ruta_csv: Path):
        """Constructor: Inicializa el objeto y el control perimetral de estados."""
        self.ruta = Path(ruta_csv)
        self.df_original = None
        self.df = None
        self.SEP = "=" * 60

    def cargar_datos(self):
        """Lee el dataset crudo y valida su integridad inicial."""
        if not self.ruta.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.ruta}")
        
        self.df_original = pd.read_csv(self.ruta, sep=";")
        if self.df_original.empty:
            raise ValueError(f"El dataset está vacío: {self.ruta}")
        
        # Generamos la copia de trabajo inmutable en el origen
        self.df = self.df_original.copy()
        print(f"[OK] Ingesta exitosa. Dimensiones: {self.df.shape[0]} filas × {self.df.shape[1]} columnas.")
        return self

    def explorar_dataset(self):
        """Diagnóstico estático completo del estado actual de la matriz de características."""
        if self.df is None:
            print("[ALERTA] No hay datos cargados para explorar.")
            return self

        print(f"{self.SEP}\n[1] TIPOS DE DATOS\n{self.SEP}")
        print(self.df.dtypes.to_string())

        print(f"\n{self.SEP}\n[2] INFORMACIÓN GENERAL\n{self.SEP}")
        self.df.info()

        print(f"\n{self.SEP}\n[3] VALORES NULOS POR COLUMNA\n{self.SEP}")
        nulos = self.df.isna().sum()
        pct = (nulos / len(self.df) * 100).round(2)
        print(pd.DataFrame({'Nulos': nulos, 'Porcentaje (%)': pct}).to_string())

        print(f"\n{self.SEP}\n[4] CEROS EN COLUMNAS CLÍNICAS (biológicamente imposibles)\n{self.SEP}")
        cols_clinicas = ['Glucose', 'BloodPressure', 'BMI', 'SkinThickness', 'Insulin']
        for col in cols_clinicas:
            if col in self.df.columns:
                n = (pd.to_numeric(self.df[col], errors='coerce') == 0).sum()
                print(f"  {col:<30}: {n} ceros")

        print(f"\n{self.SEP}\n[5] VALORES CENTINELA Y OUTLIERS EXTREMOS\n{self.SEP}")
        print(f"  Glucose  > 300  : {(self.df['Glucose'] > 300).sum()} filas (centinela 999)")
        print(f"  Age      > 100  : {(self.df['Age'] > 100).sum()} filas (centinela 150)")
        print(f"  BMI      > 60   : {(self.df['BMI'] > 60).sum()} filas")
        
        n_interrogante = (self.df['BloodPressure'].astype(str) == '?').sum()
        n_unidad = self.df['BloodPressure'].astype(str).str.contains('mmHg', na=False).sum()
        print(f"  BloodPressure '?'   : {n_interrogante} filas")
        print(f"  BloodPressure 'mmHg': {n_unidad} filas con unidad embebida")

        print(f"\n{self.SEP}\n[6] FILAS DUPLICADAS\n{self.SEP}")
        print(f"  Total duplicadas: {self.df.duplicated().sum()}")

        print(f"\n{self.SEP}\n[7] ESTADÍSTICOS DESCRIPTIVOS\n{self.SEP}")
        print(self.df.describe().round(3).to_string())

        print(f"\n{self.SEP}\n[8] DISTRIBUCIÓN VARIABLE OBJETIVO (Outcome)\n{self.SEP}")
        conteo = self.df['Outcome'].value_counts()
        pct_o = self.df['Outcome'].value_counts(normalize=True).mul(100).round(2)
        print(pd.DataFrame({'Conteo': conteo, '%': pct_o}).to_string())
        return self

    def eliminar_columnas(self, columnas: list):
        """Elimina del estado interno columnas con calidad insuficiente."""
        if self.df is not None:
            self.df = self.df.drop(columns=columnas)
            print(f"[COLUMNAS ELIMINADAS] {columnas}")
            print(f"  Columnas restantes: {list(self.df.columns)}")
        return self

    def castear_bloodpressure(self):
        """Limpia y convierte de forma vectorizada la columna BloodPressure."""
        if self.df is not None:
            self.df['BloodPressure'] = (
                self.df['BloodPressure']
                .astype(str)
                .str.replace(r'\s*mmHg', '', regex=True)
                .str.strip()
            )
            self.df['BloodPressure'] = pd.to_numeric(self.df['BloodPressure'], errors='coerce')
            print("[CASTING BloodPressure]")
            print(f"  Tipo resultante : {self.df['BloodPressure'].dtype}")
            print(f"  NaN en BP       : {self.df['BloodPressure'].isna().sum()}  (de '?' y valores no numéricos)")
        return self

    def reemplazar_invalidos(self):
        """Sustituye ceros imposibles y valores de error centinela por NaN."""
        if self.df is not None:
            cols_ceros = ['Glucose', 'BloodPressure', 'BMI', 'Insulin']
            print("[CEROS IMPOSIBLES → NaN]")
            for col in cols_ceros:
                if col in self.df.columns:
                    n = (self.df[col] == 0).sum()
                    self.df[col] = self.df[col].replace(0, np.nan)
                    print(f"  {col:<20}: {n:4d} ceros reemplados")

            print("\n[VALORES CENTINELA / OUTLIERS EXTREMOS → NaN]")
            n_g = (self.df['Glucose'] > 300).sum()
            self.df['Glucose'] = self.df['Glucose'].where(self.df['Glucose'] <= 300, np.nan)
            print(f"  Glucose > 300              : {n_g:4d} → NaN")

            n_a = (self.df['Age'] > 100).sum()
            self.df['Age'] = self.df['Age'].where(self.df['Age'] <= 100, np.nan)
            print(f"  Age > 100 (centinela 150) : {n_a:4d} → NaN")

            n_b_alto = (self.df['BMI'] > 60).sum()
            n_b_bajo = ((self.df['BMI'] < 10) & (self.df['BMI'] > 0)).sum()
            self.df['BMI'] = self.df['BMI'].where(self.df['BMI'] <= 60, np.nan)
            self.df['BMI'] = self.df['BMI'].where((self.df['BMI'] >= 10) | (self.df['BMI'].isna()), np.nan)
            print(f"  BMI > 60                   : {n_b_alto:4d} → NaN")
            print(f"  BMI < 10 (error digitación): {n_b_bajo:4d} → NaN")

            print(f"\n  NaN totales tras este paso: {self.df.isna().sum().sum()}")
        return self

    def eliminar_duplicados(self):
        """Elimina filas exactamente duplicadas manteniendo la consistencia de índices."""
        if self.df is not None:
            n_antes = len(self.df)
            self.df = self.df.drop_duplicates(keep='first').reset_index(drop=True)
            n_elim = n_antes - len(self.df)
            print(f"[DUPLICADOS]  Antes: {n_antes} | Eliminadas: {n_elim} | Después: {len(self.df)}")
        return self

    def imputar_mediana(self, columnas: list):
        """Orquesta la imputación por tendencia central robusta sobre columnas con NaN."""
        if self.df is not None:
            print("[IMPUTACIÓN POR MEDIANA]")
            for col in columnas:
                if col not in self.df.columns:
                    continue
                n = self.df[col].isna().sum()
                med = self.df[col].median()
                self.df[col] = self.df[col].fillna(med)
                estado = f"{n:4d} NaN → mediana = {med:.3f}" if n > 0 else "sin NaN"
                print(f"  {col:<28}: {estado}")
            print(f"\n  NaN restantes en el dataset: {self.df.isna().sum().sum()}")
        return self

    def validar_post_limpieza(self):
        """Ejecuta los asserts de rangos biológicos críticos PRE-escalamiento."""
        if self.df is None:
            return self

        print('REVISIÓN COLUMNA POR COLUMNA')
        for col in self.df.columns:
            print(f"\n{'='*50}")
            print(f'Columna       : {col}')
            print(f'Tipo          : {self.df[col].dtype}')
            print(f'Nulos         : {self.df[col].isnull().sum()}')
            print(f'Valores únicos: {self.df[col].nunique()}')

        print(f"\n{'='*50}")
        total_nulos = self.df.isna().sum().sum()
        print(f'NaN totales restantes: {total_nulos}')
        if total_nulos == 0:
            print('✓ Sin valores faltantes — dataset listo para transformaciones.')

        print(f"\n{'='*50}")
        print('ASSERTS DE RANGOS BIOLÓGICOS (pre-escalamiento):')

        assert self.df['Age'].between(0, 100).all(), 'Age fuera del rango válido [0, 100]'
        print('✓ Age en rango válido [0, 100]')

        assert (self.df['Glucose'] > 0).all(), 'Hay valores de Glucose ≤ 0 — imputación incompleta'
        print('✓ Glucose > 0 en todas las filas')

        assert (self.df['BloodPressure'] > 0).all(), 'Hay valores de BloodPressure ≤ 0 — imputación incompleta'
        print('✓ BloodPressure > 0 en todas las filas')

        assert (self.df['BMI'] > 0).all() and (self.df['BMI'] <= 60).all(), \
            f'BMI fuera del rango válido (0, 60]: min={self.df["BMI"].min():.2f}'
        print(f'✓ BMI en rango válido (0, 60]: min={self.df["BMI"].min():.2f}, max={self.df["BMI"].max():.2f}')

        assert self.df.duplicated().sum() == 0, 'Hay filas duplicadas'
        print('✓ Sin filas duplicadas')

        assert self.df.isna().sum().sum() == 0, 'Quedan valores NaN'
        print('✓ Sin NaN en el dataset')

        print(f"\n{'='*50}\n  TODAS LAS VALIDACIONES PASARON EXITOSAMENTE\n{'='*50}")
        return self

    def analizar_rangos(self, columnas: list):
        """Audita anomalías de dominio en rangos de valor menores o iguales a cero."""
        if self.df is None:
            return None
        resumen = pd.DataFrame({
            'Variable': columnas,
            'Valores <= 0': [(self.df[c] <= 0).sum() for c in columnas],
            'Porcentaje (%)': [round((self.df[c] <= 0).sum() / len(self.df) * 100, 2) for c in columnas],
        })
        return resumen.sort_values('Porcentaje (%)', ascending=False).reset_index(drop=True)

    def detectar_outliers_iqr(self, columnas: list):
        """Identifica la dispersión y cantidad de outliers basándose en la métrica IQR."""
        if self.df is None:
            return None
        resultado = []
        for col in columnas:
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1
            li = q1 - 1.5 * iqr
            ls = q3 + 1.5 * iqr
            n = ((self.df[col] < li) | (self.df[col] > ls)).sum()
            resultado.append([col, n])
        return pd.DataFrame(resultado, columns=['Variable', 'Cantidad de Outliers']) \
                 .sort_values('Cantidad de Outliers', ascending=False).reset_index(drop=True)

    def crear_variables_derivadas(self):
        """Construye las segmentaciones de rango clínico para AgeGroup y BMI_Category."""
        if self.df is not None:
            self.df['AgeGroup'] = pd.cut(
                self.df['Age'],
                bins=[0, 29, 44, 59, 200],
                labels=['18-29', '30-44', '45-59', '60+'],
                right=True
            )
            self.df['BMI_Category'] = pd.cut(
                self.df['BMI'],
                bins=[0, 18.5, 25.0, 30.0, 200],
                labels=['Bajo_peso', 'Normal', 'Sobrepeso', 'Obesidad'],
                right=True
            )
            print("[VARIABLES DERIVADAS]")
            print("  AgeGroup:\n", self.df['AgeGroup'].value_counts().sort_index().to_string())
            print("  BMI_Category:\n", self.df['BMI_Category'].value_counts().sort_index().to_string())
        return self

    def codificar_categoricas(self, columnas: list):
        """Aplica One-Hot Encoding controlando la multicolinealidad con drop_first."""
        if self.df is not None:
            print('[ONE-HOT ENCODING]')
            for col in columnas:
                n_antes = self.df.shape[1]
                dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True, dtype=int)
                self.df = pd.concat([self.df, dummies], axis=1)
                cols_nuevas = list(dummies.columns)
                print(f'  {col} → {cols_nuevas} ({len(cols_nuevas)} columnas nuevas)')
            print(f'\n  Columnas antes: {n_antes} | Columnas después: {self.df.shape[1]}')
        return self

    def escalar_variables(self, columnas: list):
        """Aplica StandardScaler in-place preservando la dimensionalidad compacta."""
        if self.df is not None:
            scaler = StandardScaler()
            self.df[columnas] = scaler.fit_transform(self.df[columnas])
            print("[ESCALAMIENTO StandardScaler]")
            print(f"  Columnas escaladas: {columnas}")
            print("\n  Verificación — media y desviación estándar post-escalamiento:")
            print(f"  (media ≈ 0 y std ≈ 1 confirman aplicación correcta)")
        return self

    def validar_dataset_final(self):
        """Protocolo completo de validación técnica del tensor resultante."""
        if self.df is None:
            return self

        COLS_BASE = ['Pregnancies', 'Glucose', 'BloodPressure', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
        COLS_ESCALADAS = ['Pregnancies', 'Glucose', 'BloodPressure', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

        print('=' * 55 + '\nVALIDACIÓN TÉCNICA FINAL\n' + '=' * 55)

        # 1 — Sin NaN en columnas base
        n_nan = self.df[COLS_BASE].isna().sum().sum()
        assert n_nan == 0, f'Quedan {n_nan} NaN en columnas base'
        print('✓ Sin NaN en columnas numéricas base')

        # 2 — Sin duplicados
        n_dup = self.df.duplicated().sum()
        assert n_dup == 0, f'Hay {n_dup} filas duplicadas'
        print('✓ Sin filas duplicadas')

        # 3 — Outcome en {0, 1}
        vals = set(self.df['Outcome'].unique())
        assert vals.issubset({0, 1}), f'Outcome contiene valores inesperados: {vals}'
        print('✓ Outcome solo contiene {0, 1}')

        # 4 — Coherencia dimensional
        assert len(self.df) <= len(self.df_original), 'El dataset final tiene más filas que el original'
        diff = len(self.df_original) - len(self.df)
        print(f'✓ Coherencia dimensional: {len(self.df_original)} → {len(self.df)} ({diff} filas eliminadas)')

        # 5 — Desempeño matemático de escalas continuas
        for col in COLS_ESCALADAS:
            media = self.df[col].mean()
            std = self.df[col].std()
            assert abs(media) < 1e-6, f'{col}: media = {media:.6f} (esperado ≈ 0)'
            assert abs(std - 1) < 0.01, f'{col}: std = {std:.6f} (esperado ≈ 1)'
        print(f'✓ {len(COLS_ESCALADAS)} columnas escaladas con media≈0 y std≈1')

        # 6 — Aislamiento del vector objetivo
        assert self.df['Outcome'].isin([0, 1]).all(), 'Outcome parece haber sido escalado por error'
        print('✓ Outcome conserva valores binarios {0, 1} (no fue escalado)')

        print(f'\n{"-" * 55}\nINFORMACIÓN DEL DATASET FINAL (df.info()):\n{"-" * 55}')
        self.df.info()
        print('\n' + '=' * 55 + '\n  TODAS LAS VALIDACIONES PASARON EXITOSAMENTE\n' + '=' * 55)
        return self

    def resumen_comparativo(self):
        """Genera el reporte tabular de trazabilidad evolutiva RAW vs PROCESADO."""
        if self.df is None or self.df_original is None:
            return

        COLS_BASE = ['Pregnancies', 'Glucose', 'BloodPressure', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
        resumen = pd.DataFrame({
            'Métrica': ['Filas', 'Columnas', 'NaN totales', 'Duplicados', 'Tipo BloodPressure'],
            'RAW (original)': [
                self.df_original.shape[0],
                self.df_original.shape[1],
                self.df_original.isna().sum().sum(),
                self.df_original.duplicated().sum(),
                str(self.df_original['BloodPressure'].dtype),
            ],
            'Procesado (final)': [
                self.df.shape[0],
                self.df.shape[1],
                self.df[COLS_BASE].isna().sum().sum(),
                self.df.duplicated().sum(),
                str(self.df['BloodPressure'].dtype),
            ],
        })

        print("=" * 60 + "\nCOMPARACIÓN RAW vs PROCESADO\n" + "=" * 60)
        print(resumen.to_string(index=False))

        print("\nDistribución final de Outcome:")
        conteo = self.df['Outcome'].value_counts()
        pct = self.df['Outcome'].value_counts(normalize=True).mul(100).round(2)
        print(pd.DataFrame({'Conteo': conteo, '%': pct}).to_string())
        return self

    def exportar_dataset(self, ruta_destino: Path):
        """Exporta el activo procesado purificado y realiza una validación de relectura física."""
        if self.df is not None:
            ruta_dest = Path(ruta_destino)
            ruta_dest.parent.mkdir(parents=True, exist_ok=True)
            self.df.to_csv(ruta_dest, index=False, encoding='utf-8')

            print("=" * 55 + "\nEXPORTACIÓN COMPLETADA\n" + "=" * 55)
            print(f"  Archivo   : {ruta_dest}")
            print(f"  Filas     : {self.df.shape[0]}")
            print(f"  Columnas  : {self.df.shape[1]}")
            print(f"  Tamaño    : {ruta_dest.stat().st_size / 1024:.1f} KB")

            df_check = pd.read_csv(ruta_dest)
            assert df_check.shape == self.df.shape, f"Dimensiones al releer ({df_check.shape}) ≠ DataFrame ({self.df.shape})"
            print(f"\n✓ Verificación: {df_check.shape[0]} filas × {df_check.shape[1]} cols — coincide.")

            print("\nColumnas del dataset exportado:")
            for col in self.df.columns:
                print(f"  - {col:<28} [{self.df[col].dtype}]")
        return self

    def obtener_dataframe(self):
        """Devuelve el DataFrame en su estado actual (Necesario para el Method Chaining)."""
        return self.df


# ==============================================================================
# 3. SUBCLASE ESPECIALIZADA: POLIMORFISMO APLICADO (Exigencia de Herencia)
# ==============================================================================

class PreprocesadorClinicoAvanzado(PreprocesadorDiabetes):
    """
    Clase especializada que extiende la funcionalidad base.
    Implementa polimorfismo para modificar la estrategia de descarte por una 
    estrategia de conservación avanzada en variables clínicas fragmentadas.
    """
    def tratar_skin_thickness_polimorfico(self):
        """
        Especialización de pipeline: En lugar de eliminar SkinThickness,
        recupera la columna reemplazando ceros por NaN e imputando con su propia mediana.
        """
        if self.df is not None:
            self.df['SkinThickness'] = self.df['SkinThickness'].replace(0, np.nan)
            mediana_skin = self.df['SkinThickness'].median()
            self.df['SkinThickness'] = self.df['SkinThickness'].fillna(mediana_skin)
            print(f"[POLIMORFISMO] SkinThickness recuperada e imputada con mediana propia ({mediana_skin:.3f})")
        return self