import streamlit as st
import pandas as pd

# ======================================================================
# 1. CONFIGURACIÓN DE PESOS (Arquitectura de Ingeniería)
# ======================================================================
# Clasificamos las variables por importancia diagnóstica
PESOS = {
    "edad_inicio": 3.0, "manifestacion": 3.0, "lateralidad": 3.0,  # CORE (Del AG)
    "desarrollo": 1.5, "fiebre": 1.5, "antecedentes": 1.5,        # CONFIRMATORIOS
    "ocurrencia": 1.0, "frecuencia": 1.0, "parto": 1.0, "trato": 1.0 # CONTEXTUALES
}

# ======================================================================
# 2. BASE DE CONOCIMIENTO (Sustentada en ILAE y tu Minería de Datos)
# ======================================================================
CONOCIMIENTO_EXPERTOS = [
    {
        "diag": "EIDEE (Ohtahara/Early Myoclonic)",
        "perfil": {
            "edad_inicio": "Neonatal (<30 días)", "manifestacion": "Tónica", "lateralidad": "Bilateral/Simétrica",
            "desarrollo": "Retraso/Estancamiento", "fiebre": "No", "antecedentes": "Sí",
            "ocurrencia": "Clusters (Ráfagas)", "frecuencia": "Muy Alta (>50 al día)", 
            "parto": "Complicado/Asfixia", "trato": "Farmacorresistente"
        }
    },
    {
        "diag": "Dravet Syndrome",
        "perfil": {
            "edad_inicio": "Lactancia (1-12 meses)", "manifestacion": "Clónica", "lateralidad": "Unilateral/Cambiante",
            "desarrollo": "Normal Inicial", "fiebre": "Sí (Desencadenante)", "antecedentes": "No",
            "ocurrencia": "Prolongadas (>5 min)", "frecuencia": "Alta", 
            "parto": "Normal", "trato": "Pobre"
        }
    },
    {
        "diag": "SeLNE (Autolimitado/Benigno)",
        "perfil": {
            "edad_inicio": "Neonatal (<30 días)", "manifestacion": "Clónica", "lateralidad": "Migratoria",
            "desarrollo": "Normal", "fiebre": "No", "antecedentes": "Sí (Familiar)",
            "ocurrencia": "Breves", "frecuencia": "Baja/Media", 
            "parto": "Normal", "trato": "Excelente"
        }
    }
]

# ======================================================================
# 3. MOTOR DE INFERENCIA PONDERADO
# ======================================================================
def calcular_diagnostico(datos_paciente):
    puntos_maximos = sum(PESOS.values())
    resultados = []

    for sindrome in CONOCIMIENTO_EXPERTOS:
        puntos_obtenidos = 0
        evidencia = []
        
        for var, peso in PESOS.items():
            if datos_paciente[var] == sindrome['perfil'][var]:
                puntos_obtenidos += peso
                evidencia.append(var)
        
        # Fórmula: $C_f = \frac{\sum (W_i \cdot X_i)}{\sum W_i} \times 100$
        confianza = (puntos_obtenidos / puntos_maximos) * 100
        resultados.append({"diagnostico": sindrome['diag'], "confianza": confianza, "match": evidencia})
    
    return sorted(resultados, key=lambda x: x['confianza'], reverse=True)

# ======================================================================
# 4. INTERFAZ DE USUARIO (Streamlit)
# ======================================================================
st.set_page_config(page_title="UAT - CDSS Epilepsy", layout="wide")
st.title("🛡️ Sistema de Soporte al Diagnóstico de Epilepsia Neonatal")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Cuestionario Clínico")
    with st.container(border=True):
        p_edad = st.selectbox("1. Edad de inicio:", ["Neonatal (<30 días)", "Lactancia (1-12 meses)", "Infancia"])
        p_manif = st.selectbox("2. Manifestación principal:", ["Tónica", "Clónica", "Espasmos", "Focal", "Ausencia"])
        p_lat = st.selectbox("3. Lateralidad:", ["Bilateral/Simétrica", "Unilateral/Cambiante", "Migratoria"])
        p_des = st.radio("4. Desarrollo psicomotor:", ["Normal", "Normal Inicial", "Retraso/Estancamiento"], horizontal=True)
        p_fie = st.radio("5. ¿Relación con fiebre?", ["Sí", "No"], horizontal=True)
        p_ant = st.radio("6. Antecedentes familiares:", ["Sí", "No"], horizontal=True)
        p_ocu = st.selectbox("7. ¿Cómo ocurren?", ["Breves", "Prolongadas (>5 min)", "Clusters (Ráfagas)"])
        p_fre = st.selectbox("8. Frecuencia:", ["Baja", "Media", "Alta", "Muy Alta (>50 al día)"])
        p_par = st.radio("9. Complicaciones en parto:", ["Normal", "Complicado/Asfixia"], horizontal=True)
        p_tra = st.selectbox("10. Respuesta al tratamiento:", ["Excelente", "Variable", "Pobre", "Farmacorresistente"])

with col2:
    st.header("📊 Resultado del Análisis")
    
    paciente = {
        "edad_inicio": p_edad, "manifestacion": p_manif, "lateralidad": p_lat,
        "desarrollo": p_des, "fiebre": p_fie, "antecedentes": p_ant,
        "ocurrencia": p_ocu, "frecuencia": p_fre, "parto": p_par, "trato": p_tra
    }
    
    if st.button("🚀 Calcular Probabilidad Diagnóstica"):
        diagnosticos = calcular_diagnostico(paciente)
        
        for d in diagnosticos:
            # Color dinámico según confianza
            color = "green" if d['confianza'] > 70 else "orange" if d['confianza'] > 40 else "red"
            
            st.subheader(f"{d['diagnostico']}")
            st.progress(d['confianza'] / 100)
            st.write(f"**Confianza:** :{color}[{d['confianza']:.1f}%]")
            st.write(f"**Coincidencias clave:** {', '.join(d['match'])}")
            st.markdown("---")