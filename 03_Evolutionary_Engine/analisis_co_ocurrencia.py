import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from itertools import combinations
from collections import Counter

# 1. Conexión a tu Bóveda (PostgreSQL 18)
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)

def analizar_co_ocurrencia():
    print("--- 🧠 Generando Mapa de Relaciones Clínicas ---")
    
    # Traemos todas las entidades y sus IDs de documento
    query = text("SELECT articulo_id, entidad_clinica FROM clinical_entities")
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    if df.empty:
        print("❌ No hay datos suficientes para el análisis.")
        return

    # Agrupamos los síntomas por cada PDF
    documentos = df.groupby('articulo_id')['entidad_clinica'].apply(list).tolist()

    # Generamos todas las combinaciones posibles de pares dentro de cada documento
    parejas_totales = []
    for sintomas in documentos:
        # Ordenamos alfabéticamente para que (A,B) sea igual a (B,A)
        combinaciones = list(combinations(sorted(set(sintomas)), 2))
        parejas_totales.extend(combinaciones)

    # Contamos cuántas veces aparece cada pareja
    conteo_parejas = Counter(parejas_totales)
    top_parejas = conteo_parejas.most_common(15)

    # --- VISUALIZACIÓN 1: Gráfica de Barras ---
    nombres = [f"{p[0]} + {p[1]}" for p, c in top_parejas]
    valores = [c for p, c in top_parejas]

    plt.figure(figsize=(12, 6))
    plt.bar(nombres, valores, color='orchid')
    plt.xticks(rotation=45, ha='right')
    plt.title('Relaciones Clínicas más Fuertes (Co-ocurrencia)')
    plt.ylabel('Número de Documentos')
    plt.tight_layout()
    plt.savefig('relaciones_clinicas.png')

    # --- VISUALIZACIÓN 2: Heatmap (Matriz de Calor) ---
    entidades_unicas = sorted(df['entidad_clinica'].unique())
    matriz = pd.DataFrame(0, index=entidades_unicas, columns=entidades_unicas)

    for (p1, p2), c in conteo_parejas.items():
        matriz.loc[p1, p2] = c
        matriz.loc[p2, p1] = c

    plt.figure(figsize=(14, 10))
    sns.heatmap(matriz, annot=True, cmap='YlGnBu', fmt='d')
    plt.title('Matriz de Co-ocurrencia de Síntomas')
    plt.tight_layout()
    plt.savefig('matriz_calor_sintomas.png')

    print("🚀 ¡Análisis completado! Revisa 'relaciones_clinicas.png' y 'matriz_calor_sintomas.png'.")

if __name__ == "__main__":
    analizar_co_ocurrencia()