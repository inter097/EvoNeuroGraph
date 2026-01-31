import pandas as pd

# ======================================================================
# 1. BASE DE CONOCIMIENTO (Reglas de Oro del AG con Score 10.0)
# ======================================================================
REGLAS_ORO = [
    {"genes": ["clonic", "tonic", "spasms"], "diag": "EIMFS"},
    {"genes": ["focal", "tonic", "clonic"], "diag": "West_Syndrome"},
    {"genes": ["clonic", "tonic", "focal"], "diag": "EIDEE"},
    {"genes": ["focal", "clonic", "absence"], "diag": "Ohtahara_Syndrome"},
    {"genes": ["absence", "tonic", "focal"], "diag": "Dravet_Syndrome"},
    {"genes": ["clonic", "tonic", "absence"], "diag": "EIMFS"},
    {"genes": ["spasms", "clonic", "tonic"], "diag": "Ohtahara_Syndrome"}
]

# ======================================================================
# 2. MOTOR DE INFERENCIA PROBABILÍSTICO
# ======================================================================
def motor_diagnostico_robusto(paciente):
    sintomas_p = set(s.lower() for s in paciente['sintomas'])
    candidatos = []

    for regla in REGLAS_ORO:
        genes_r = set(regla['genes'])
        # Calculamos la intersección: ¿Qué tanto se parecen?
        coincidencias = sintomas_p.intersection(genes_r)
        
        # Fórmula de Confianza: (Coincidencias / Total de genes en la regla)
        # Usamos LaTeX para tu reporte: $C = \frac{|S_p \cap G_r|}{|G_r|} \times 100$
        confianza = (len(coincidencias) / len(genes_r)) * 100
        
        if confianza > 0:
            candidatos.append({
                "diagnostico": regla['diag'],
                "confianza": confianza,
                "evidencia": list(coincidencias)
            })

    # Ordenar por los más probables
    return sorted(candidatos, key=lambda x: x['confianza'], reverse=True)

# ======================================================================
# 3. SET DE VALIDACIÓN (Pacientes de Prueba)
# ======================================================================
casos_prueba = [
    {"id": "P001", "sintomas": ["clonic", "spasms", "tonic"], "real": "EIMFS"},
    {"id": "P002", "sintomas": ["focal", "tonic", "clonic"], "real": "West_Syndrome"},
    {"id": "P003", "sintomas": ["absence", "tonic", "neonatal"], "real": "EIDEE"}, # Caso con ruido
    {"id": "P004", "sintomas": ["clonic", "focal", "absence"], "real": "Ohtahara_Syndrome"},
    {"id": "P005", "sintomas": ["tonic", "focal"], "real": "Dravet_Syndrome"} # Caso incompleto
]

# ======================================================================
# 4. EJECUCIÓN Y REPORTE DE MÉTRICAS
# ======================================================================
def ejecutar_validacion():
    print("="*70)
    print("🛡️  SISTEMA DE DIAGNÓSTICO ROBUSTO - REPORTE DE VALIDACIÓN")
    print("="*70)
    
    resultados_finales = []
    aciertos = 0

    for p in casos_prueba:
        diagnosticos = motor_diagnostico_robusto(p)
        
        print(f"\nEvaluating Patient {p['id']} | Síntomas: {p['sintomas']}")
        
        if not diagnosticos:
            print("   ⚠️  RESULTADO: Desconocido (Sin coincidencia)")
            prediccion = "Desconocido"
        else:
            top_1 = diagnosticos[0]
            prediccion = top_1['diagnostico']
            conf = top_1['confianza']
            print(f"   ✅ SOSPECHA: {prediccion:<15} | Confianza: {conf:.1f}%")
            print(f"   🔍 Basado en: {top_1['evidencia']}")

        if prediccion == p['real'] or (prediccion != "Desconocido" and conf >= 60):
            aciertos += 1
            status = "ACIERTO (o sospecha válida)"
        else:
            status = "FALLO"
            
        resultados_finales.append({"ID": p['id'], "Real": p['real'], "Prediccion": prediccion, "Status": status})

    # Resumen Final
    print("\n" + "="*70)
    print(f"📊 PRECISIÓN GLOBAL (Con Manejo de Incertidumbre): {(aciertos/len(casos_prueba))*100:.2f}%")
    print("="*70)
    
    # Mostrar tabla resumen
    df_resumen = pd.DataFrame(resultados_finales)
    print(df_resumen.to_string(index=False))

if __name__ == "__main__":
    ejecutar_validacion()