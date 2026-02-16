# 📋 Guía de Ejecución - ETL Pipeline Inmobiliario

Esta guía te explica paso a paso cómo ejecutar el proyecto ETL.

## ✅ Requisitos Previos

- Python 3.8 o superior instalado
- pip (gestor de paquetes de Python)

## 🚀 Pasos para Ejecutar el Proyecto

### **Paso 1: Navegar al directorio del proyecto**

Abre una terminal (PowerShell, CMD, o Terminal de Cursor) y ve al directorio del proyecto:

```bash
cd C:\Users\josef\github\etl-pipeline-inmobiliario
```

### **Paso 2: Instalar las dependencias**

Instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

**Dependencias que se instalarán:**
- `pandas` - Para manipulación de datos
- `numpy` - Para operaciones numéricas
- `openpyxl` - Para leer archivos Excel
- `pyarrow` - Para formato Parquet

### **Paso 3: Generar datos de ejemplo (Opcional pero recomendado)**

Si no tienes datos propios, genera datos de ejemplo:

```bash
python generate_sample_data.py
```

**Esto creará:**
- Archivo: `data/raw/propiedades_raw.csv`
- 150 registros de propiedades inmobiliarias de ejemplo
- Datos con diferentes tipos, precios, superficies, etc.

### **Paso 4: Ejecutar el Pipeline ETL**

Ejecuta el pipeline principal:

```bash
python etl_pipeline.py
```

**El pipeline realizará:**
1. **Extract (Extracción)**: Lee los datos desde `data/raw/propiedades_raw.csv`
2. **Transform (Transformación)**: 
   - Limpia y normaliza los datos
   - Calcula métricas derivadas (precio/m², categorías)
   - Valida la calidad de los datos
   - Detecta outliers y duplicados
3. **Load (Carga)**: Guarda los datos procesados en `data/processed/propiedades_procesadas.csv`

### **Paso 5: Verificar los resultados**

Los datos procesados estarán en:
```
data/processed/propiedades_procesadas.csv
```

**Columnas nuevas generadas:**
- `precio_m2`: Precio por metro cuadrado
- `categoria_precio`: Categorización (Económico, Medio, Premium)
- `antiguedad_dias`: Días desde la publicación
- `mes_publicacion`: Mes de publicación
- `año_publicacion`: Año de publicación
- `ratio_precio_superficie`: Ratio precio/superficie

## 📊 Ejemplo de Salida

Cuando ejecutes el pipeline, verás algo como esto:

```
============================================================
INICIANDO PIPELINE ETL
============================================================
Extrayendo datos desde: data\raw\propiedades_raw.csv
Datos extraídos: 150 registros, 10 columnas
Iniciando validaciones de calidad de datos...
✓ Todas las validaciones de calidad pasaron exitosamente
Iniciando transformación de datos...
Transformación completada: 150 registros procesados
Cargando datos en: data\processed\propiedades_procesadas.csv
✓ Datos cargados exitosamente
============================================================
PIPELINE ETL COMPLETADO EXITOSAMENTE
============================================================

REPORTE DE PROCESAMIENTO
============================================================
fecha_procesamiento: 2026-02-16 14:25:34
registros_originales: 150
registros_procesados: 150
columnas: 16
validaciones_fallidas: 0
errores: []
```

## 🔧 Usar tus Propios Datos

Si quieres procesar tus propios datos:

1. **Prepara tu archivo CSV** con las siguientes columnas (mínimas):
   - `id_propiedad`: Identificador único
   - `precio`: Precio de la propiedad
   - `tipo_propiedad`: Tipo (Departamento, Casa, etc.)
   - `superficie_m2`: Superficie en metros cuadrados
   - `fecha_publicacion`: Fecha de publicación (formato: YYYY-MM-DD)

2. **Coloca el archivo** en: `data/raw/tu_archivo.csv`

3. **Modifica** `etl_pipeline.py` línea 291:
   ```python
   input_file = 'data/raw/tu_archivo.csv'  # Cambia aquí
   ```

4. **Ejecuta** el pipeline normalmente:
   ```bash
   python etl_pipeline.py
   ```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError"
**Solución**: Asegúrate de tener datos en `data/raw/`. Ejecuta:
```bash
python generate_sample_data.py
```

### Error de codificación en Windows
**Solución**: Ya está corregido en el código. Si persiste, asegúrate de usar Python 3.8+

## 📝 Notas Adicionales

- Los logs del proceso se muestran en la consola
- Los datos originales NO se modifican (solo se leen)
- Los datos procesados se guardan en una carpeta separada
- El pipeline es idempotente: puedes ejecutarlo múltiples veces

## 🎯 Próximos Pasos

Una vez que el proyecto funcione:
1. Revisa los datos procesados en `data/processed/`
2. Puedes importar el CSV a Power BI, Excel, o cualquier herramienta de visualización
3. Personaliza las transformaciones según tus necesidades

---

**¡Listo!** Ahora tienes un pipeline ETL funcionando que demuestra tus habilidades en Ingeniería de Datos. 🚀
