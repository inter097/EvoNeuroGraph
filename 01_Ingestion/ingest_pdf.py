import fitz  # PyMuPDF
from sqlalchemy import create_engine, text
import os

# 1. Configuración de la Bóveda (PostgreSQL 18)
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)

# 2. Diccionario Clínico-Observacional (Bilingüe)
# Enfocado en lo que un médico general puede "ver" o preguntar
TERMINOS_CLINICOS = [
    # Edad de inicio (Componente 1)
    "neonatal", "infancy", "childhood", "adolescent", "onset",
    # Patrones de crisis (Componente 2)
    "tonic", "clonic", "spasms", "migrating", "focal", "generalized",
    "atonic", "absence", "motor", "awareness", "prolonged",
    # Antecedentes y Factores (Componentes 7 y 10)
    "family history", "febrile seizure", "fever", "infection", "sleep deprivation",
    # Comorbilidades y Desarrollo (Componentes 4 y 11)
    "regression", "delay", "retardation", "autism", "cognitive",
    # Términos en Español (para cobertura local)
    "tónica", "clónica", "espasmos", "migratoria", "neonatal", "fiebre"
]

def procesar_biblioteca_clinica(folder_path):
    print(f"--- 🏥 Iniciando Ingesta para Atención Primaria ---")
    
    if not os.path.exists(folder_path):
        print(f"❌ La carpeta '{folder_path}' no existe.")
        return

    archivos = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    print(f"📂 Encontrados {len(archivos)} documentos.")

    for archivo in archivos:
        path = os.path.join(folder_path, archivo)
        try:
            # Extracción de texto
            doc = fitz.open(path)
            contenido = ""
            for pagina in doc:
                contenido += pagina.get_text()
            
            # Inserción en la tabla raw_knowledge
            with engine.begin() as conn:
                query = text("""
                    INSERT INTO raw_knowledge (fuente, categoria, contenido_texto, metadata)
                    VALUES (:fuente, :cat, :texto, :meta)
                    RETURNING id
                """)
                result = conn.execute(query, {
                    "fuente": archivo,
                    "cat": "Clinica_Atencion_Primaria",
                    "texto": contenido,
                    "meta": '{"observacional": true, "ignore_eeg": true}'
                })
                raw_id = result.fetchone()[0]

                # Minería inmediata de términos clínicos
                texto_lower = contenido.lower()
                for termino in TERMINOS_CLINICOS:
                    conteo = texto_lower.count(termino)
                    if conteo > 0:
                        q_entidad = text("""
                            INSERT INTO clinical_entities (articulo_id, entidad_clinica, tipo_entidad, confianza_ia)
                            VALUES (:id, :entidad, 'Observacion_Clinica', 1.0)
                        """)
                        conn.execute(q_entidad, {"id": raw_id, "entidad": termino})
            
            print(f"✅ {archivo}: Procesado e indexado.")

        except Exception as e:
            print(f"⚠️ Error procesando {archivo}: {e}")

if __name__ == "__main__":
    procesar_biblioteca_clinica("referencias")