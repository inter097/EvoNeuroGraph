# 🧠 Discovery of Knowledge in Neonatal Epilepsy using Evolutionary Computing and Semantic Web

Este proyecto de tesis (Maestría en Ciencia de Datos, UAT) presenta un **Sistema de Soporte a la Decisión Clínica (CDSS)** diseñado para médicos de atención primaria. El sistema integra minería de datos de literatura especializada (ILAE), modelado semántico y algoritmos genéticos para el diagnóstico de encefalopatías epilépticas.

---

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en cuatro módulos funcionales que representan el pipeline de descubrimiento de conocimiento:

1.  **01_Ingestion**: Extracción de entidades clínicas desde guías de práctica clínica (PDF) hacia una base de datos relacional (**PostgreSQL 18**).
2.  **02_Knowledge_Engineering**: Modelado de la ontología en OWL y puentes de datos (Bridges) para la integración de grafos de conocimiento.
3.  **03_Evolutionary_Engine**: Algoritmo Genético (AG) para la optimización y descubrimiento de reglas clínicas basadas en co-ocurrencia y frecuencia.
4.  **04_CDSS_App**: Interfaz de usuario robusta construida con **Streamlit** que utiliza un motor de inferencia ponderado.

---

## 🛠️ Stack Tecnológico

* **Lenguaje**: Python 3.10+
* **Base de Datos**: PostgreSQL 18 + SQLAlchemy
* **Ingeniería Semántica**: Owlready2 (OWL/SWRL)
* **Ciencia de Datos**: Scikit-learn, Pandas, NumPy
* **Interfaz**: Streamlit
* **Hardware**: Optimizado para ejecución en NVIDIA RTX 4060

---

## 🚀 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
   cd tu-repositorio