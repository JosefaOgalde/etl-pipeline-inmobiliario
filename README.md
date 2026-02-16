# 🏢 ETL Pipeline - Procesamiento de Datos Inmobiliarios

Este proyecto demuestra un **proceso ETL completo** (Extract, Transform, Load) para el procesamiento y análisis de datos inmobiliarios, implementando mejores prácticas de **calidad y gobernanza de datos**.

## 📋 Descripción

Pipeline ETL desarrollado en Python que procesa datos de propiedades inmobiliarias, aplicando:
- ✅ Validaciones de calidad de datos
- ✅ Transformaciones y enriquecimiento de información
- ✅ Detección de outliers y anomalías
- ✅ Normalización y limpieza de datos
- ✅ Generación de métricas y reportes

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas y vectorizadas
- **SQL** - Consultas y transformaciones (simuladas en código)

## 📁 Estructura del Proyecto

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

## 🚀 Instalación y Uso

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/JosefaOgalde/etl-pipeline-inmobiliario.git
cd etl-pipeline-inmobiliario
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Generar datos de ejemplo (opcional)

```bash
python generate_sample_data.py
```

### 4. Ejecutar el pipeline ETL

```bash
python etl_pipeline.py
```

## 🔍 Características Principales

### Extract (Extracción)
- Lectura de datos desde múltiples fuentes (CSV, Excel)
- Manejo de errores y logging detallado
- Validación de formatos de entrada

### Transform (Transformación)
- **Limpieza de datos**: Normalización de texto, eliminación de duplicados
- **Enriquecimiento**: Cálculo de métricas derivadas (precio/m², categorías)
- **Validaciones de calidad**: 
  - Detección de valores nulos críticos
  - Validación de rangos y outliers
  - Identificación de duplicados
- **Transformaciones numéricas**: Uso de NumPy para operaciones vectorizadas

### Load (Carga)
- Exportación a múltiples formatos (CSV, Parquet)
- Generación de reportes de procesamiento
- Logging completo del proceso

## 📊 Validaciones de Calidad Implementadas

1. **Valores Nulos**: Verificación de campos críticos
2. **Rangos de Valores**: Validación de precios y superficies positivas
3. **Detección de Outliers**: Uso de método IQR (Interquartile Range)
4. **Duplicados**: Identificación de registros duplicados por ID
5. **Consistencia**: Validación de relaciones entre campos

## 💡 Ejemplo de Uso

```python
from etl_pipeline import ETLPipeline

# Crear instancia del pipeline
pipeline = ETLPipeline(
    input_path='data/raw/propiedades_raw.csv',
    output_path='data/processed/propiedades_procesadas.csv'
)

# Ejecutar proceso completo
report = pipeline.run()

# Ver reporte
print(report)
```

## 📈 Métricas Generadas

El pipeline genera automáticamente:
- Número de registros procesados
- Estadísticas descriptivas de campos numéricos
- Reporte de validaciones y errores encontrados
- Métricas de calidad de datos

## 🎯 Aplicación en Contexto Empresarial

Este pipeline demuestra competencias clave para roles de **Ingeniería de Datos**:

- ✅ Diseño y desarrollo de procesos ETL
- ✅ Implementación de gobernanza de datos
- ✅ Validación y calidad de datos
- ✅ Trabajo con Python, Pandas y NumPy
- ✅ Documentación profesional y código mantenible

## 📝 Notas Técnicas

- El código sigue principios de **clean code** y **buenas prácticas**
- Implementa **logging** para trazabilidad completa
- Manejo robusto de **errores y excepciones**
- Código **modular y escalable**

## 👤 Autor

**Josefa Ogalde**  
Ingeniera en Informática

---

## 🔗 Enlaces

- [Repositorio GitHub](https://github.com/JosefaOgalde)
- [LinkedIn](#) - *Agregar tu perfil*

---

*Este proyecto fue desarrollado como demostración de competencias técnicas en Ingeniería de Datos.*
