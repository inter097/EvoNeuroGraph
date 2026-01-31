from owlready2 import *
from sqlalchemy import create_engine, text
import pandas as pd

# 1. Configuración de entrada
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)
onto = get_ontology("Epilepsy_Primary_Care.owl").load()

def vincular_grafo():
    print("--- 🔗 Construyendo el Grafo de Conocimiento Real ---")
    
    with onto:
        # Definimos los Síndromes (Basado en ILAE 2022 y Chiang et al.)
        # Estos son los objetivos para el médico general en Ciudad Victoria
        sindromes_map = {
            "EIDEE": ["neonatal", "tonic", "spasms"],
            "Dravet_Syndrome": ["infancy", "clonic", "febrile seizure"],
            "EIMFS": ["infancy", "migrating", "focal"]
        }

        for nombre_s, sintomas_s in sindromes_map.items():
            # CREACIÓN: Aquí realmente nace el individuo en la clase
            sindrome_ind = onto.EpilepsySyndrome(nombre_s)
            print(f"🏥 Configurando Síndrome: {nombre_s}")
            
            for s in sintomas_s:
                sintoma_ind = onto.search_one(name=s)
                if sintoma_ind:
                    # VINCULACIÓN: Aquí se traza la flecha lógica
                    sindrome_ind.has_symptom.append(sintoma_ind)
                    print(f"   -> Flecha trazada hacia: {s}")

    # 3. Guardar el progreso
    onto.save(file="Epilepsy_Knowledge_Graph.owl", format="rdfxml")
    print("\n✅ ¡Grafo Terminado! Ahora sí, abre Protégé y verás las conexiones.")

if __name__ == "__main__":
    vincular_grafo()