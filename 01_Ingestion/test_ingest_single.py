import fitz  # PyMuPDF
from sqlalchemy import create_engine, text

# 1. Configuración de tu conexión
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)

def prueba_ingesta_unica(path_al_pdf):
    print(f"--- 🧪 Iniciando Prueba de Ingesta Única ---")
    
    try:
        # 2. Extraer texto del PDF
        doc = fitz.open(path_al_pdf)
        texto_extraido = ""
        for pagina in doc:
            texto_extraido += pagina.get_text()
        
        print(f"✅ Texto extraído con éxito ({len(texto_extraido)} caracteres).")

        # 3. Subir a PostgreSQL 18
        nombre_archivo = path_al_pdf.split("/")[-1]
        with engine.begin() as conn:
            query = text("""
                INSERT INTO raw_knowledge (fuente, categoria, contenido_texto, metadata)
                VALUES (:fuente, :cat, :texto, :meta)
            """)
            conn.execute(query, {
                "fuente": nombre_archivo,
                "cat": "Prueba_Piloto",
                "texto": texto_extraido,
                "meta": '{"status": "test", "metodo": "single_file"}'
            })
            
        print(f"🚀 ¡Éxito! El archivo '{nombre_archivo}' ya está en la Bóveda de Conocimiento.")

    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

if __name__ == "__main__":
    # Cambia esto por el nombre de tu PDF (debe estar en la misma carpeta o dar la ruta completa)
    prueba_ingesta_unica("mi_archivo_de_prueba.pdf")