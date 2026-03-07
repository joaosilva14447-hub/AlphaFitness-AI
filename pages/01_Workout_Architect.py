import streamlit as st
import pandas as pd

# 1. Configuração de Elite
st.set_page_config(page_title="Workout Architect | Alpha Fitness", layout="wide")

# 2. Paleta de Cores Alpha
AQUA = "#00FBFF"
BLUE = "#3D5AFE"

# 3. Estilização CSS para manter o branding
st.markdown(f"""
<style>
    .main {{ background-color: #0F0F0F; }}
    .stSelectbox, .stMultiSelect {{ color: {AQUA}; }}
    h1, h2, h3 {{ color: {BLUE}; font-family: 'Inter', sans-serif; }}
    .exercise-card {{
        background-color: #161616;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {BLUE};
        margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h1>✦ 𝓦𝓸𝓻𝓴𝓸𝓾𝓽 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 4. Inputs de Performance (Sidebar)
with st.sidebar:
    st.header("✦ Training Parameters")
    level = st.select_slider("Experience Level", options=["Beginner", "Intermediate", "Advanced"])
    
    # O "Filtro de Inteligência"
    equipment = st.multiselect(
        "Available Equipment", 
        ["Bodyweight", "Dumbbells", "Barbell", "Cables", "Machines"],
        default=["Bodyweight", "Dumbbells"]
    )
    
    split = st.radio("Routine Type", ["Full Body", "Push / Pull / Legs", "Upper / Lower"])

# 5. Base de Dados de Exercícios (O Cérebro do Robô)
# Cada exercício tem uma etiqueta de equipamento para o filtro
db = {
    "Push": [
        {"name": "Push-ups", "eq": "Bodyweight", "reps": "3x Max"},
        {"name": "Dumbbell Bench Press", "eq": "Dumbbells", "reps": "4x 10-12"},
        {"name": "Barbell Overhead Press", "eq": "Barbell", "reps": "3x 8"},
        {"name": "Tricep Pushdowns", "eq": "Cables", "reps": "3x 15"},
        {"name": "Chest Press Machine", "eq": "Machines", "reps": "3x 12"}
    ],
    "Pull": [
        {"name": "Pull-ups / Chin-ups", "eq": "Bodyweight", "reps": "3x Max"},
        {"name": "One-Arm Dumbbell Row", "eq": "Dumbbells", "reps": "4x 12"},
        {"name": "Barbell Deadlift", "eq": "Barbell", "reps": "3x 5"},
        {"name": "Lat Pulldown", "eq": "Cables", "reps": "3x 10"},
        {"name": "Seated Row Machine", "eq": "Machines", "reps": "3x 12"}
    ],
    "Legs": [
        {"name": "Bodyweight Squats", "eq": "Bodyweight", "reps": "4x 20"},
        {"name": "Goblet Squats", "eq": "Dumbbells", "reps": "3x 12"},
        {"name": "Barbell Back Squat", "eq": "Barbell", "reps": "5x 5"},
        {"name": "Leg Extension", "eq": "Machines", "reps": "3x 15"},
        {"name": "Cable Pull-throughs", "eq": "Cables", "reps": "3x 12"}
    ]
}

# 6. Lógica de Filtragem e Geração
st.subheader(f"✦ Your Alpha Routine: {split} ({level})")

# Criamos colunas para uma visualização limpa
col1, col2 = st.columns([2, 1])

with col1:
    # Mapeamento do treino baseado no Split escolhido
    active_categories = []
    if split == "Full Body":
        active_categories = ["Push", "Pull", "Legs"]
    elif split == "Push / Pull / Legs":
        active_categories = ["Push", "Pull", "Legs"] # Simplificado para o exemplo
    else:
        active_categories = ["Push", "Pull"]

    for category in active_categories:
        st.markdown(f"### {category} Movements")
        count = 0
        for ex in db[category]:
            if ex["eq"] in equipment:
                st.markdown(f"""
                <div class="exercise-card">
                    <span style="color:{AQUA}; font-weight:bold;">{ex['name']}</span><br>
                    <small>Equipment: {ex['eq']} | <b>Volume: {ex['reps']}</b></small>
                </div>
                """, unsafe_allow_html=True)
                count += 1
        
        if count == 0:
            st.warning(f"No {category} exercises found for the selected equipment.")

with col2:
    st.markdown(f"### ✦ High Performance Notes")
    st.info(f"""
    **Status:** {level} Protocol Active.
    
    1. **Rest Periods:** 90s for compounds, 60s for isolation.
    2. **Progressive Overload:** Focus on adding 1kg or 1 rep every session.
    3. **Tempo:** 3-0-1-0 (3s eccentric phase).
    """)
    
    if st.button("Verify Form with AI"):
        st.write("AI Computer Vision Module: *Coming Soon*")

# --- SUMMARY FOR CLIENT (English Section) ---
st.divider()
st.markdown("### ✦ Execution Summary (For Client)")
st.code(f"""
CLIENT REPORT:
- Training Split: {split}
- Goal: Hypertrophy & Neuromuscular Adaptation
- Intensity: RPE 8-9 based on {level} status.
- Primary Driver: {', '.join(equipment)} availability.
""", language="text")
