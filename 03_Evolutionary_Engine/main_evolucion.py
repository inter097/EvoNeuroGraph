import random
from sqlalchemy import create_engine, text

# 1. Configuración y Bóveda
DB_PARAMS = "postgresql+psycopg://postgres:1234@localhost:5432/Epilepsy_Knowledge_Vault"
engine = create_engine(DB_PARAMS)

EDADES = ["neonatal", "infancy", "childhood"]
SIGNOS = ["tonic", "clonic", "spasms", "migrating", "focal", "absence", "atonic", "generalized"]
SINDROMES = ["EIDEE", "Dravet_Syndrome", "EIMFS", "Ohtahara_Syndrome", "West_Syndrome"]

def crear_regla():
    return {
        "genes": [random.choice(EDADES), random.choice(SIGNOS), random.choice(SIGNOS)],
        "diagnostico": random.choice(SINDROMES),
        "fitness": 0
    }

def evaluar_fitness(regla):
    # Juez Estricto: Los 3 genes deben ser distintos y coexistir en el mismo PDF
    if len(set(regla['genes'])) < 3: return 0.0 # Penaliza reglas con signos repetidos
    
    query = text("""
        SELECT COUNT(*) FROM (
            SELECT articulo_id FROM clinical_entities 
            WHERE entidad_clinica IN (:g0, :g1, :g2)
            GROUP BY articulo_id HAVING COUNT(DISTINCT entidad_clinica) = 3
        ) as triple_check;
    """)
    with engine.connect() as conn:
        return float(conn.execute(query, {
            "g0": regla['genes'][0], "g1": regla['genes'][1], "g2": regla['genes'][2]
        }).scalar())

def evolucionar_pro(progenitores, tasa_mutacion=0.2):
    hijos = []
    while len(hijos) < len(progenitores):
        p1, p2 = random.sample(progenitores, 2)
        # Crossover de punto único
        nuevo_gen = [p1['genes'][0], p1['genes'][1], p2['genes'][2]]
        hijo = {"genes": nuevo_gen, "diagnostico": random.choice([p1['diagnostico'], p2['diagnostico']]), "fitness": 0}
        
        # Mutación más agresiva para romper mesetas
        if random.random() < tasa_mutacion:
            hijo['genes'][random.randint(0, 2)] = random.choice(SIGNOS)
        hijos.append(hijo)
    return hijos

def ejecutar_pipeline_pro(pob_size=100, gens=20):
    print(f"--- 🧬 Evolucionando Población de {pob_size} individuos ---")
    poblacion = [crear_regla() for _ in range(pob_size)]
    
    for g in range(gens):
        for r in poblacion: r['fitness'] = evaluar_fitness(r)
        poblacion = sorted(poblacion, key=lambda x: x['fitness'], reverse=True)
        
        if g % 5 == 0:
            print(f"Generación {g}: Mejor Fitness = {poblacion[0]['fitness']}")
            
        mejores = poblacion[:pob_size//2]
        poblacion = mejores + evolucionar_pro(mejores)

    print("\n" + "="*70)
    print("📋 RESULTADO FINAL: TOP 10 REGLAS CLÍNICAS OPTIMIZADAS")
    print("="*70)
    
    vistas = set()
    count = 1
    for r in poblacion:
        # Evitar imprimir reglas duplicadas en el Top 10
        regla_str = f"{r['genes']} -> {r['diagnostico']}"
        if regla_str not in vistas and count <= 10:
            print(f"{count:02d}. SI {r['genes'][0].upper()} + {r['genes'][1]} + {r['genes'][2]} "
                  f"| SOSPECHAR: {r['diagnostico']:<15} | Score: {r['fitness']}")
            vistas.add(regla_str)
            count += 1

if __name__ == "__main__":
    ejecutar_pipeline_pro()