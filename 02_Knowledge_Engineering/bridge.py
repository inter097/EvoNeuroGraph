import psycopg
import torch
import pandas as pd
from sqlalchemy import create_engine, text # Importamos 'text'

# --- 1. Configuración de la Bóveda ---
DB_NAME = "Epilepsy_Knowledge_Vault"
DB_USER = "postgres"
DB_PASS = "1234" 
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_and_wake_beast():
    print("--- 🛠️ Iniciando Sistema de Ingeniería de Conocimiento ---")
    
    # --- 2. Despertando a la RTX 4060 ---
    if torch.cuda.is_available():
        beast_name = torch.cuda.get_device_name(0)
        print(f"✅ Bestia detectada: {beast_name}")
    else:
        print("⚠️ GPU no detectada. Trabajando en modo CPU.")

    # --- 3. Probando Conexión a PostgreSQL 18 ---
    try:
        # El driver debe ser 'postgresql+psycopg' para usar la versión 3 que instalamos
        conn_string = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(conn_string)
        
        # Usamos .begin() para que gestione la transacción automáticamente
        with engine.begin() as connection:
            print(f"✅ Conexión exitosa a la base de datos: {DB_NAME}")
            
            # Usamos text() de SQLAlchemy para envolver la consulta
            test_query = text("""
                INSERT INTO raw_knowledge (fuente, categoria, contenido_texto)
                VALUES ('Sistema Local', 'Log', 'Puente de datos establecido y GPU lista.')
            """)
            
            connection.execute(test_query)
            print("🚀 Registro de prueba insertado correctamente.")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    connect_and_wake_beast()