import torch
from sqlalchemy import create_engine, text
import pandas as pd

# 1. Configuración de conexión (Asegura tu contraseña)
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)

# 2. Diccionario bilingüe (Inglés/Español) para los PDFs de la ILAE
TERMINOS_CLAVE = [
    "tonic", "clonic", "migrating", "neonatal", "seizure", 
    "encephalopathy", "onset", "spasms", "eidee", "selne", "eimfs",
    "tónica", "clónica", "migratoria", "espasmos"
]

def minar_conocimiento():
    print("--- 🧠 Iniciando Minería de Texto en la GPU ---")
    
    # Extraer el texto de la tabla raw_knowledge
    # Asegúrate de que la categoría coincida con la que usaste al subir el PDF
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text("SELECT id, contenido_texto FROM raw_knowledge"), conn)

        if df.empty:
            print("❌ No hay datos en 'raw_knowledge' para procesar.")
            return

        # Verificación de la Bestia (GPU)
        dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📍 Procesando con: {dispositivo} ({torch.cuda.get_device_name(0) if dispositivo == 'cuda' else 'CPU'})")

        hallazgos = []
        # Tomamos el último documento subido para la prueba
        texto_completo = df.iloc[-1]['contenido_texto'].lower()
        id_documento = int(df.iloc[-1]['id'])

        for termino in TERMINOS_CLAVE:
            conteo = texto_completo.count(termino)
            if conteo > 0:
                hallazgos.append({
                    "id": id_documento,
                    "entidad": termino,
                    "conteo": conteo
                })

        # 3. Guardar en clinical_entities usando 'articulo_id'
        if hallazgos:
            with engine.begin() as conn:
                for h in hallazgos:
                    query = text("""
                        INSERT INTO clinical_entities (articulo_id, entidad_clinica, tipo_entidad, confianza_ia)
                        VALUES (:id, :entidad, 'Termino_Clave', 1.0)
                    """)
                    conn.execute(query, {"id": h['id'], "entidad": h['entidad']})
            print(f"🚀 Se encontraron y guardaron {len(hallazgos)} términos clínicos con éxito.")
        else:
            print("🔍 No se encontraron términos de la lista en el documento.")

    except Exception as e:
        print(f"❌ Error durante la minería: {e}")

if __name__ == "__main__":
    minar_conocimiento()