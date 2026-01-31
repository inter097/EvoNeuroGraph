import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

# 1. Conexión a tu PostgreSQL 18
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)

def generar_reporte_clinico():
    print("--- 🩺 Generando Reporte de Signos Observables ---")
    
    query = text("""
        SELECT entidad_clinica, COUNT(*) as menciones
        FROM clinical_entities
        GROUP BY entidad_clinica
        ORDER BY menciones DESC;
    """)
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    if df.empty:
        print("🔍 No hay entidades procesadas aún.")
        return

    print("\n🏆 Top 10 Signos detectados en la literatura:")
    print(df.head(25))

    # Visualización rápida
    df.head(15).plot(kind='barh', x='entidad_clinica', y='menciones', color='teal')
    plt.title('Frecuencia de Signos Clínicos en la Biblioteca ILAE')
    plt.xlabel('Número de menciones')
    plt.ylabel('Signo / Síntoma')
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    generar_reporte_clinico()