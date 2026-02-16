"""
Script para generar datos de ejemplo para el pipeline ETL.
Útil para demostración y testing.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import random

def generate_sample_data(n_records: int = 100) -> pd.DataFrame:
    """
    Genera datos de ejemplo de propiedades inmobiliarias.
    
    Args:
        n_records: Número de registros a generar
        
    Returns:
        DataFrame con datos de ejemplo
    """
    np.random.seed(42)
    random.seed(42)
    
    # Tipos de propiedades
    tipos_propiedad = ['Departamento', 'Casa', 'Oficina', 'Local Comercial', 'Terreno']
    comunas = ['Las Condes', 'Providencia', 'Ñuñoa', 'Vitacura', 'La Reina', 
               'Santiago Centro', 'Maipú', 'Puente Alto', 'San Miguel', 'La Florida']
    estados = ['Disponible', 'Reservado', 'Vendido', 'En Remodelación']
    
    data = {
        'id_propiedad': [f'PROP-{i+1:04d}' for i in range(n_records)],
        'tipo_propiedad': np.random.choice(tipos_propiedad, n_records),
        'comuna': np.random.choice(comunas, n_records),
        'precio': np.random.normal(250000, 100000, n_records).astype(int),
        'superficie_m2': np.random.normal(80, 30, n_records).astype(int),
        'habitaciones': np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.1, 0.3, 0.3, 0.2, 0.1]),
        'banos': np.random.choice([1, 2, 3, 4], n_records, p=[0.2, 0.4, 0.3, 0.1]),
        'estado': np.random.choice(estados, n_records, p=[0.6, 0.15, 0.2, 0.05]),
        'fecha_publicacion': [
            datetime.now() - timedelta(days=random.randint(1, 365)) 
            for _ in range(n_records)
        ],
        'descripcion': [
            f"Propiedad {i+1} en excelente ubicación" 
            for i in range(n_records)
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Asegurar que los precios sean positivos
    df['precio'] = np.abs(df['precio'])
    
    # Asegurar que la superficie sea positiva
    df['superficie_m2'] = np.abs(df['superficie_m2'])
    
    # Agregar algunos valores nulos para testing de validaciones
    null_indices = np.random.choice(df.index, size=int(n_records * 0.05), replace=False)
    df.loc[null_indices, 'descripcion'] = None
    
    return df

def main():
    """Genera archivo de datos de ejemplo."""
    # Crear directorio si no existe
    data_dir = Path('data/raw')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar datos
    print("Generando datos de ejemplo...")
    df = generate_sample_data(n_records=150)
    
    # Guardar
    output_file = data_dir / 'propiedades_raw.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✓ Datos generados: {len(df)} registros")
    print(f"✓ Guardado en: {output_file}")
    print(f"\nVista previa:")
    print(df.head())

if __name__ == "__main__":
    main()
