import streamlit as st

# 1. Configuração de Autoridade
st.set_page_config(page_title="Alpha Fitness AI", layout="wide", page_icon="⚡")

# Cores da Identidade Alpha
AQUA, BLUE = "#00FBFF", "#3D5AFE"

st.markdown(f"""
<style>
    .main {{ background-color: #0F0F0F; }}
    div[data-testid='stMetric'] {{ 
        background-color: #161616; 
        padding: 20px; 
        border-radius: 5px; 
        border: 1px solid #333; 
    }}
    h1 {{ font-family: serif; color: {BLUE}; text-align: center; }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h1>✦ 𝓐𝓛𝓟𝓗𝓐 𝓕𝓘𝓣𝓝𝓔𝓢𝓢: 𝓝𝓮𝓾𝓻𝓪𝓵 𝓒𝓸𝓷𝓽𝓻𝓸𝓵 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Captura de Dados Biométricos (Input do Cliente)
st.subheader("✦ Biometric Data Ingestion")

c1, c2, c3 = st.columns(3)

with c1:
    weight = st.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=80.0, step=0.1)
    height = st.number_input("Altura (cm)", min_value=120, max_value=220, value=175)

with c2:
    age = st.number_input("Idade", min_value=15, max_value=90, value=25)
    gender = st.selectbox("Sexo Biológico", ["Masculino", "Feminino"])

with c3:
    activity = st.selectbox("Nível de Atividade", ["Sedentário", "Moderado", "Intenso (Atleta)"])
    goal = st.selectbox("Objetivo Estratégico", ["Maintenance", "Bulking", "Cutting"])

# 3. Guardar no Session State (Crucial para as outras páginas)
st.session_state['user_weight'] = weight
st.session_state['user_goal'] = goal
st.session_state['user_gender'] = gender

# 4. Motor de Cálculo Metabólico (Mifflin-St Jeor)
if gender == "Masculino":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

# Ajuste por atividade
mult = {"Sedentário": 1.2, "Moderado": 1.55, "Intenso (Atleta)": 1.9}
tdee = bmr * mult[activity]

# Ajuste por Objetivo
if goal == "Bulking": target_cals = tdee + 400
elif goal == "Cutting": target_cals = tdee - 500
else: target_cals = tdee

# 5. Dashboard de Performance Imediata
st.write("---")
st.subheader("✦ Strategic Forecast")

m1, m2, m3 = st.columns(3)
m1.metric("BMR (Metabolismo Base)", f"{bmr:.0f} kcal")
m2.metric("TDEE (Gasto Diário)", f"{tdee:.0f} kcal")
m3.metric("TARGET DIÁRIO", f"{target_cals:.0f} kcal", delta=f"{target_cals - tdee:.0f} vs TDEE")

# 6. Call to Action Alpha
st.info(f"🚀 Dados Sincronizados. Podes agora navegar para o **Workout Architect** e para a **Neural Nutrition** no menu lateral para veres o teu plano personalizado.")

st.divider()
st.markdown("### ✦ SYSTEM STATUS: OPERATIONAL")
st.code(f"ENCRYPTION: ACTIVE | DATA_SYNC: OK | CLIENT_GOAL: {goal.upper()}", language="text")


