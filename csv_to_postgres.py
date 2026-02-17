import pandas as pd
from sqlalchemy import create_engine, text
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno (opcional, si usas .env)
load_dotenv()

def create_table_from_csv(csv_file_path, table_name, schema='public'):
    """
    Crea una tabla en PostgreSQL a partir de un archivo CSV
    
    Args:
        csv_file_path (str): Ruta al archivo CSV
        table_name (str): Nombre de la tabla a crear
        schema (str): Esquema de la base de datos
    """
    
    # Configuración de conexión a la base de datos
    db_config = {
        'host': os.getenv('DB_HOST', 'postgres'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'data_analysis'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres123')
    }
    
    # Crear conexión a PostgreSQL
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    
    try:
        # Crear engine de SQLAlchemy
        engine = create_engine(connection_string)
        
        print(f"📂 Leyendo archivo CSV: {csv_file_path}")
        
        # Leer el CSV
        df = pd.read_csv(csv_file_path)
        
        print(f"📊 CSV cargado: {len(df)} filas, {len(df.columns)} columnas")
        print(f"📋 Columnas encontradas: {', '.join(df.columns)}")
        
        # Mostrar tipos de datos inferidos
        print("\n🔍 Tipos de datos inferidos:")
        for col, dtype in df.dtypes.items():
            print(f"  - {col}: {dtype}")
        
        # Verificar si la tabla ya existe
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = '{schema}' AND table_name = '{table_name}')")
            )
            table_exists = result.scalar()
        
        if table_exists:
            print(f"⚠️  La tabla '{table_name}' ya existe en el esquema '{schema}'")
            respuesta = input("¿Deseas reemplazarla? (s/n): ")
            
            if respuesta.lower() == 's':
                # Eliminar tabla si existe
                with engine.connect() as conn:
                    conn.execute(text(f"DROP TABLE {schema}.{table_name} CASCADE"))
                    conn.commit()
                print(f"🗑️  Tabla '{table_name}' eliminada")
            else:
                print("❌ Operación cancelada")
                return
        
        # Crear tabla y cargar datos
        print(f"\n📦 Creando tabla '{table_name}' y cargando datos...")
        df.to_sql(
            table_name, 
            engine, 
            schema=schema, 
            if_exists='replace', 
            index=False,
            chunksize=1000  # Cargar en lotes de 1000 filas
        )
        
        print(f"✅ ¡Datos cargados exitosamente en la tabla '{schema}.{table_name}'!")
        
        # Mostrar algunas estadísticas
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{table_name}"))
            count = result.scalar()
            print(f"📈 Total de registros en la tabla: {count}")
            
            # Mostrar las primeras 5 filas
            sample = pd.read_sql(f"SELECT * FROM {schema}.{table_name} LIMIT 5", engine)
            print("\n👀 Primeras 5 filas de la tabla:")
            print(sample.to_string())
            
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{csv_file_path}'")
        print("   Asegúrate de que el archivo existe en la ruta especificada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Configurar parámetros
    CSV_FILE = "csv.csv"  # Nombre de tu archivo CSV
    TABLE_NAME = "cwpp"    # Nombre de la tabla
    
    # Ejecutar la función
    create_table_from_csv(CSV_FILE, TABLE_NAME)
