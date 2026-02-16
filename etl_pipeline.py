"""
ETL Pipeline para datos inmobiliarios
=====================================
Pipeline para procesar y transformar datos de propiedades.
Incluye validaciones de calidad y transformaciones de negocio.

Josefa Ogalde - 2024
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """
    Pipeline ETL para procesar datos inmobiliarios.
    Maneja extracción, transformación y carga de datos con validaciones.
    """
    
    def __init__(self, input_path: str, output_path: str):
        """
        Inicializa el pipeline ETL.
        
        Args:
            input_path: Ruta del archivo de entrada
            output_path: Ruta del archivo de salida
        """
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.df_raw = None
        self.df_processed = None
        self.validation_errors = []
        
    def extract(self) -> pd.DataFrame:
        """
        Extrae los datos desde la fuente.
        
        Returns:
            DataFrame con los datos extraídos
        """
        logger.info(f"Extrayendo datos desde: {self.input_path}")
        
        try:
            # Por ahora lee desde archivos, pero podría venir de BD o API
            if self.input_path.suffix == '.csv':
                self.df_raw = pd.read_csv(self.input_path, encoding='utf-8')
            elif self.input_path.suffix in ['.xlsx', '.xls']:
                self.df_raw = pd.read_excel(self.input_path)
            else:
                raise ValueError(f"Formato no soportado: {self.input_path.suffix}")
            
            logger.info(f"Datos extraídos: {len(self.df_raw)} registros, {len(self.df_raw.columns)} columnas")
            return self.df_raw
            
        except Exception as e:
            logger.error(f"Error en extracción: {str(e)}")
            raise
    
    def validate_data_quality(self, df: pd.DataFrame) -> bool:
        """
        Valida la calidad de los datos según reglas de negocio.
        
        Args:
            df: DataFrame a validar
            
        Returns:
            True si pasa todas las validaciones
        """
        logger.info("Iniciando validaciones de calidad de datos...")
        self.validation_errors = []
        
        # Valores nulos en columnas críticas
        critical_columns = ['id_propiedad', 'precio', 'tipo_propiedad']
        for col in critical_columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    self.validation_errors.append(
                        f"Columna '{col}': {null_count} valores nulos encontrados"
                    )
        
        # Validar rangos de valores (precios negativos no tienen sentido)
        if 'precio' in df.columns:
            negative_prices = (df['precio'] < 0).sum()
            if negative_prices > 0:
                self.validation_errors.append(
                    f"Precios negativos encontrados: {negative_prices}"
                )
            
            # Detectar outliers con método IQR (más robusto que usar desviación estándar)
            Q1 = df['precio'].quantile(0.25)
            Q3 = df['precio'].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df['precio'] < (Q1 - 1.5 * IQR)) | 
                       (df['precio'] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                logger.warning(f"Posibles outliers detectados: {outliers}")
        
        # Buscar duplicados por ID
        duplicates = df.duplicated(subset=['id_propiedad']).sum() if 'id_propiedad' in df.columns else 0
        if duplicates > 0:
            self.validation_errors.append(f"Registros duplicados encontrados: {duplicates}")
        
        if self.validation_errors:
            logger.warning(f"Validaciones fallidas: {len(self.validation_errors)}")
            for error in self.validation_errors:
                logger.warning(f"  - {error}")
            return False
        
        logger.info("✓ Todas las validaciones de calidad pasaron exitosamente")
        return True
    
    def transform(self) -> pd.DataFrame:
        """
        Transforma los datos aplicando reglas de negocio y limpieza.
        
        Returns:
            DataFrame transformado
        """
        logger.info("Iniciando transformación de datos...")
        
        if self.df_raw is None:
            raise ValueError("Debe ejecutar extract() primero")
        
        df = self.df_raw.copy()
        
        # Limpiar texto: normalizar y capitalizar
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = df[col].astype(str).str.strip().str.title()
        
        # Normalizar precios (a veces vienen con símbolos $ o comas)
        if 'precio' in df.columns:
            df['precio'] = pd.to_numeric(
                df['precio'].astype(str).str.replace(r'[^\d.]', '', regex=True),
                errors='coerce'
            )
            # Calcular precio por m² - útil para comparar propiedades
            if 'superficie_m2' in df.columns:
                df['precio_m2'] = np.where(
                    df['superficie_m2'] > 0,
                    df['precio'] / df['superficie_m2'],
                    np.nan
                )
        
        # Categorizar precios según rangos del mercado chileno
        if 'precio' in df.columns:
            df['categoria_precio'] = np.select(
                [
                    df['precio'] < 100000,
                    (df['precio'] >= 100000) & (df['precio'] < 300000),
                    df['precio'] >= 300000
                ],
                ['Económico', 'Medio', 'Premium'],
                default='No definido'
            )
        
        # Extraer info de fechas para análisis temporal
        if 'fecha_publicacion' in df.columns:
            df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'], errors='coerce')
            df['antiguedad_dias'] = (datetime.now() - df['fecha_publicacion']).dt.days
            df['mes_publicacion'] = df['fecha_publicacion'].dt.month
            df['año_publicacion'] = df['fecha_publicacion'].dt.year
        
        # Ratio precio/superficie (similar a precio_m2 pero con otro nombre por compatibilidad)
        if 'superficie_m2' in df.columns and 'precio' in df.columns:
            df['ratio_precio_superficie'] = np.where(
                df['superficie_m2'] > 0,
                df['precio'] / df['superficie_m2'],
                np.nan
            )
        
        # Eliminar duplicados
        if 'id_propiedad' in df.columns:
            df = df.drop_duplicates(subset=['id_propiedad'], keep='first')
        
        self.df_processed = df
        logger.info(f"Transformación completada: {len(df)} registros procesados")
        
        return df
    
    def load(self) -> None:
        """
        Carga los datos transformados al destino final.
        """
        if self.df_processed is None:
            raise ValueError("Debe ejecutar transform() primero")
        
        logger.info(f"Cargando datos en: {self.output_path}")
        
        # Crear directorio si no existe
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar según formato
        if self.output_path.suffix == '.csv':
            self.df_processed.to_csv(self.output_path, index=False, encoding='utf-8-sig')
        elif self.output_path.suffix == '.parquet':
            self.df_processed.to_parquet(self.output_path, index=False)
        else:
            self.df_processed.to_csv(self.output_path, index=False, encoding='utf-8-sig')
        
        logger.info("✓ Datos cargados exitosamente")
    
    def generate_summary_report(self) -> dict:
        """
        Genera un reporte resumen del proceso ETL.
        
        Returns:
            Diccionario con métricas del proceso
        """
        if self.df_processed is None:
            return {}
        
        report = {
            'fecha_procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'registros_originales': len(self.df_raw) if self.df_raw is not None else 0,
            'registros_procesados': len(self.df_processed),
            'columnas': len(self.df_processed.columns),
            'validaciones_fallidas': len(self.validation_errors),
            'errores': self.validation_errors
        }
        
        # Métricas adicionales si existen columnas numéricas
        numeric_cols = self.df_processed.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            report['estadisticas'] = self.df_processed[numeric_cols].describe().to_dict()
        
        return report
    
    def run(self) -> dict:
        """
        Ejecuta el pipeline ETL completo.
        
        Returns:
            Reporte del proceso
        """
        logger.info("=" * 60)
        logger.info("INICIANDO PIPELINE ETL")
        logger.info("=" * 60)
        
        try:
            # Extract
            self.extract()
            
            # Validar datos originales
            is_valid = self.validate_data_quality(self.df_raw)
            if not is_valid:
                logger.warning("Se detectaron problemas de calidad, pero continuando con la transformación...")
            
            # Transform
            self.transform()
            
            # Validar datos transformados
            self.validate_data_quality(self.df_processed)
            
            # Load
            self.load()
            
            # Reporte
            report = self.generate_summary_report()
            
            logger.info("=" * 60)
            logger.info("PIPELINE ETL COMPLETADO EXITOSAMENTE")
            logger.info("=" * 60)
            
            return report
            
        except Exception as e:
            logger.error(f"Error en pipeline ETL: {str(e)}")
            raise


def main():
    """Función principal - ejecuta el pipeline completo."""
    # Rutas de archivos (cambiar según necesidad)
    input_file = 'data/raw/propiedades_raw.csv'
    output_file = 'data/processed/propiedades_procesadas.csv'
    
    pipeline = ETLPipeline(input_path=input_file, output_path=output_file)
    report = pipeline.run()
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("REPORTE DE PROCESAMIENTO")
    print("=" * 60)
    for key, value in report.items():
        if key != 'estadisticas':
            print(f"{key}: {value}")
    
    return pipeline


if __name__ == "__main__":
    main()
