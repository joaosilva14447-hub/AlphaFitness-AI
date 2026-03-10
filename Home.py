import streamlit as st
import plotly.graph_objects as go

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

# 2. Captura de Dados Biométricos (Grelha 3x2)
st.subheader("✦ Biometric Data Ingestion")

r1_c1, r1_c2, r1_c3 = st.columns(3)
with r1_c1:
    weight = st.number_input("Peso Atual (kg)", min_value=40.0, max_value=200.0, value=80.0, step=0.1)
with r1_c2:
    height = st.number_input("Altura (cm)", min_value=120, max_value=220, value=175)
with r1_c3:
    age = st.number_input("Idade", min_value=15, max_value=90, value=25)

r2_c1, r2_c2, r2_c3 = st.columns(3)
with r2_c1:
    gender = st.selectbox("Sexo Biológico", ["Masculino", "Feminino"])
with r2_c2:
    activity = st.selectbox("Nível de Atividade", ["Sedentário", "Moderado", "Intenso (Atleta)"])
with r2_c3:
    goal = st.selectbox("Objetivo Estratégico", ["Maintenance", "Bulking", "Cutting"])

# 3. Sincronização de Dados para as outras páginas
st.session_state['user_weight'] = weight
st.session_state['user_goal'] = goal

# 4. Motor de Cálculo Metabólico e Macros
if gender == "Masculino":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

mult = {"Sedentário": 1.2, "Moderado": 1.55, "Intenso (Atleta)": 1.9}
tdee = bmr * mult[activity]

if goal == "Bulking": target_cals = tdee + 400
elif goal == "Cutting": target_cals = tdee - 500
else: target_cals = tdee

# Cálculo de Macros (Os "Outros Fatores")
prot = weight * 2.2
fats = weight * 0.8
carbs = (target_cals - (prot * 4) - (fats * 9)) / 4

# 5. Dashboard de Performance (Métricas e Gráfico)
st.write("---")
st.subheader("✦ Strategic Forecast & Macro Partitioning")

m1, m2, m3 = st.columns(3)
m1.metric("TDEE (Manutenção)", f"{tdee:.0f} kcal")
m2.metric("TARGET DIÁRIO", f"{target_cals:.0f} kcal", delta=f"{target_cals - tdee:.0f}")
m3.metric("ÁGUA MÍNIMA", f"{(weight * 35) / 1000:.1f} L")

# Layout de Gráfico e Detalhes de Macros
col_graph, col_macros = st.columns([1.5, 1])

with col_graph:
    # Gráfico de Rosca (Donut Chart)
    fig = go.Figure(data=[go.Pie(
        labels=['Proteína', 'Carbo', 'Gordura'],
        values=[prot*4, carbs*4, fats*9],
        hole=.6,
        marker_colors=[AQUA, BLUE, "#FFFFFF"],
        textinfo='label+percent'
    )])
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=350,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_macros:
    st.write("### ✦ Macronutrient Targets")
    st.markdown(f"**Proteína:** `{prot:.0f}g` (Equivalente a {prot/30:.1f} doses)")
    st.markdown(f"**Carbo:** `{carbs:.0f}g` (Energia Primária)")
    st.markdown(f"**Gordura:** `{fats:.0f}g` (Suporte Hormonal)")
    st.info("💡 Estes valores foram injetados no teu plano de nutrição.")

st.divider()
st.markdown("### ✦ SYSTEM STATUS: OPERATIONAL")
st.code(f"USER_WEIGHT: {weight}KG | TARGET: {target_cals:.0f}KCAL | GOAL: {goal.upper()}", language="text")



