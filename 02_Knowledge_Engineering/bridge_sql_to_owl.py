from owlready2 import *
import psycopg
from sqlalchemy import create_engine, text
import pandas as pd

# 1. Configuración de Conexiones
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)
ONTOLOGY_FILE = "Epilepsy_Primary_Care.owl" # Nombre de tu archivo de Protégé

def build_knowledge_graph():
    print("--- 🦉 Iniciando Mapeo de Ontología (Web Semántica) ---")
    
    # 2. Cargar o crear la Ontología
    # Si el archivo no existe, creamos una base con las clases del artículo
    onto = get_ontology("http://test.org/epilepsy.owl").load() if os.path.exists(ONTOLOGY_FILE) else get_ontology("http://test.org/epilepsy.owl")

    with onto:
        # Definimos las Clases principales (basadas en el paper de Chiang)
        class EpilepsySyndrome(Thing): pass
        class SeizureType(Thing): pass
        class ClinicalSign(Thing): pass
        class OnsetAge(Thing): pass
        
        # Propiedades (Relaciones)
        class has_symptom(ObjectProperty):
            domain = [EpilepsySyndrome]
            range  = [ClinicalSign, SeizureType]

    # 3. Leer hallazgos de SQL
    query = text("SELECT DISTINCT entidad_clinica, tipo_entidad FROM clinical_entities")
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    # 4. Mapeo Automático
    print(f"📦 Mapeando {len(df)} entidades encontradas...")
    for index, row in df.iterrows():
        nombre = row['entidad_clinica'].replace(" ", "_")
        
        with onto:
            # Creamos el individuo según su tipo
            if row['entidad_clinica'] in ['neonatal', 'infancy', 'childhood']:
                new_item = OnsetAge(nombre)
            elif row['entidad_clinica'] in ['tonic', 'clonic', 'spasms']:
                new_item = SeizureType(nombre)
            else:
                new_item = ClinicalSign(nombre)
                
    # 5. Guardar la Ontología
    onto.save(file = ONTOLOGY_FILE, format = "rdfxml")
    print(f"✅ ¡Éxito! Ontología actualizada y guardada como '{ONTOLOGY_FILE}'.")
    print("🚀 Ahora puedes abrir este archivo en Protégé para ver tus datos.")

if __name__ == "__main__":
    build_knowledge_graph()