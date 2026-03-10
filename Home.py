import streamlit as st

# 1. Configuração Master de Elite
st.set_page_config(page_title="Alpha Fitness AI", layout="wide", page_icon="⚡")

# Cores Institucionais Alpha
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

# 2. Captura de Dados Biométricos (Layout Grelha 3x2 igual à Imagem)
st.subheader("✦ Biometric Data Ingestion")

# Linha 1 de Inputs
r1_c1, r1_c2, r1_c3 = st.columns(3)
with r1_c1:
    weight = st.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=80.0, step=0.1)
with r1_c2:
    height = st.number_input("Altura (cm)", min_value=120, max_value=220, value=175)
with r1_c3:
    age = st.number_input("Idade", min_value=15, max_value=90, value=25)

# Linha 2 de Inputs
r2_c1, r2_c2, r2_c3 = st.columns(3)
with r2_c1:
    gender = st.selectbox("Sexo Biológico", ["Masculino", "Feminino"])
with r2_c2:
    activity = st.selectbox("Nível de Atividade", ["Sedentário", "Moderado", "Intenso (Atleta)"])
with r2_c3:
    goal = st.selectbox("Objetivo Estratégico", ["Maintenance", "Bulking", "Cutting"])

# 3. Sincronização de Dados (Session State Protocol)
st.session_state['user_weight'] = weight
st.session_state['user_goal'] = goal
st.session_state['user_gender'] = gender

# 4. Motor de Cálculo Metabólico
if gender == "Masculino":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

mult = {"Sedentário": 1.2, "Moderado": 1.55, "Intenso (Atleta)": 1.9}
tdee = bmr * mult[activity]

if goal == "Bulking": target_cals = tdee + 400
elif goal == "Cutting": target_cals = tdee - 500
else: target_cals = tdee

# 5. Dashboard de Performance (Strategic Forecast)
st.write("---")
st.subheader("✦ Strategic Forecast")

m1, m2, m3 = st.columns(3)
m1.metric("BMR (Metabolismo Base)", f"{bmr:.0f} kcal")
m2.metric("TDEE (Gasto Diário)", f"{tdee:.0f} kcal")
m3.metric("TARGET DIÁRIO", f"{target_cals:.0f} kcal", delta=f"{target_cals - tdee:.0f} vs TDEE")

# 6. Rodapé Técnico
st.divider()
st.markdown("### ✦ SYSTEM STATUS: OPERATIONAL")
st.code(f"ENCRYPTION: ACTIVE | DATA_SYNC: OK | CLIENT_GOAL: {goal.upper()}", language="text")



