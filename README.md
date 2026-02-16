# ETL Pipeline - Procesamiento de Datos Inmobiliarios

Pipeline ETL desarrollado en Python para procesar y transformar datos de propiedades inmobiliarias. Incluye validaciones de calidad, transformaciones de negocio y generación de métricas derivadas.

## Descripción

Este proyecto implementa un pipeline ETL completo que:
- Extrae datos desde archivos CSV/Excel
- Valida la calidad de los datos (nulos, duplicados, outliers)
- Transforma y enriquece la información (cálculo de métricas, categorización)
- Carga los datos procesados en formato estructurado

Desarrollado para demostrar competencias en ingeniería de datos y procesamiento de información.

## Tecnologías

- Python 3.8+
- Pandas - para manipulación de DataFrames
- NumPy - operaciones numéricas vectorizadas

## Estructura del Proyecto

```
etl-pipeline-inmobiliario/
│
├── etl_pipeline.py          # Pipeline ETL principal
├── generate_sample_data.py  # Generador de datos de ejemplo
├── requirements.txt         # Dependencias del proyecto
├── README.md               # Documentación
│
└── data/
    ├── raw/                # Datos sin procesar
    │   └── propiedades_raw.csv
    └── processed/          # Datos transformados
        └── propiedades_procesadas.csv
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/JosefaOgalde/etl-pipeline-inmobiliario.git
cd etl-pipeline-inmobiliario

# Instalar dependencias
pip install -r requirements.txt

# Generar datos de ejemplo (opcional)
python generate_sample_data.py

# Ejecutar pipeline
python etl_pipeline.py
```

## Funcionalidades

**Extract (Extracción)**
- Lee datos desde CSV y Excel
- Manejo de errores con logging

**Transform (Transformación)**
- Limpieza y normalización de texto
- Cálculo de métricas: precio/m², categorización de precios
- Extracción de información temporal (mes, año, antigüedad)
- Validación de calidad: nulos, duplicados, outliers

**Load (Carga)**
- Exporta a CSV y Parquet
- Genera reporte de procesamiento

## Validaciones de Calidad

- Verificación de valores nulos en columnas críticas
- Validación de rangos (precios y superficies positivas)
- Detección de outliers usando método IQR
- Identificación de registros duplicados

## Uso

```python
from etl_pipeline import ETLPipeline

pipeline = ETLPipeline(
    input_path='data/raw/propiedades_raw.csv',
    output_path='data/processed/propiedades_procesadas.csv'
)

report = pipeline.run()
print(report)
```

## Métricas Generadas

- Número de registros procesados
- Estadísticas descriptivas
- Reporte de validaciones y errores

## Autor

Josefa Ogalde - Ingeniera en Informática

---

*Proyecto desarrollado para demostrar competencias en procesamiento de datos y ETL.*
