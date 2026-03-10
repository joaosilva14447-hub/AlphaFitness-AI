import streamlit as st
import plotly.graph_objects as go

# Configuração de Elite
st.set_page_config(page_title="Neural Nutrition | Alpha Fitness", layout="wide")

AQUA, BLUE = "#00FBFF", "#3D5AFE"

# Recuperação de Dados da Home (Session State)
# Se não houver dados, usamos valores padrão de segurança
weight = st.session_state.get('user_weight', 80)
goal = st.session_state.get('user_goal', 'Maintenance')

st.markdown(f"<h1>✦ 𝓝𝓮𝓾𝓻𝓪𝓵 𝓝𝓾𝓽𝓻𝓲𝓽𝓲𝓸𝓷 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# --- LÓGICA DE PARTIÇÃO DE NUTRIENTES ---
with st.sidebar:
    st.header("✦ Nutrition Protocol")
    meals = st.slider("Refeições por dia", 3, 6, 4)
    strategy = st.selectbox("Estratégia", ["Balanced", "Low Carb / High Fat", "High Carb / Low Fat"])

# Cálculo simplificado para demonstração
# (Numa fase avançada, puxamos os cálculos exatos da Home)
base_cals = 2500 if goal == "Maintenance" else 2800 if goal == "Bulking" else 2200
prot = weight * 2.2
fats = weight * 0.8
carbs = (base_cals - (prot * 4) - (fats * 9)) / 4

# --- VISUALIZAÇÃO DE CARGA MACRO ---
st.subheader("✦ Daily Fuel Distribution")
fig = go.Figure(data=[
    go.Pie(labels=['Proteína', 'Carbo', 'Gordura'], 
           values=[prot*4, carbs*4, fats*9],
           hole=.6,
           marker_colors=[AQUA, BLUE, "#FFFFFF"])
])
fig.update_layout(template="plotly_dark", paper_bgcolor="#0F0F0F", showlegend=True)
st.plotly_chart(fig, use_container_width=True)

# --- REFEIÇÕES GERADAS PELO ROBÔ ---
st.subheader("✦ Neural Meal Plan")

meal_cols = st.columns(2)
for i in range(meals):
    with meal_cols[i % 2]:
        with st.expander(f"Refeição {i+1} - Protocolo Alpha", expanded=True):
            st.markdown(f"""
            **Alvos da Refeição:**
            - Proteína: {prot/meals:.1f}g
            - Carboidratos: {carbs/meals:.1f}g
            - Gorduras: {fats/meals:.1f}g
            """)
            st.info("💡 Sugestão: Frango Grelhado + Arroz Basmati + Abacate")

# --- PROTOCOLO DE EXECUÇÃO ---
st.divider()
st.markdown("### ✦ MISSION EXECUTION PROTOCOL")
st.code(f"""
NUTRITION BRIEFING:
- Current Strategy: {strategy}
- Frequency: {meals} Feeding Windows
- Caloric Target: {base_cals} kcal
- Focus: Optimization of nutrient partitioning for {goal}.
""", language="text")
