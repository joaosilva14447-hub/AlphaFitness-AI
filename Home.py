import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração Master
st.set_page_config(page_title="AI Fitness Robot - Alpha Performance", layout="wide")

# Estética "Hedge Fund" (Aqua & Blue)
AQUA = "#00FBFF"
BLUE = "#3D5AFE"

st.markdown(f"""
<style>
    .main {{ background-color: #0F0F0F; }}
    div[data-testid='stMetric'] {{ 
        background-color: #161616; padding: 20px; border-radius: 10px; border: 1px solid #333; 
    }}
    h1, h2, h3 {{ font-family: serif; color: white; }}
</style>
""", unsafe_allow_html=True)

# Título de Elite
st.markdown(f"<h1 style='text-align: center; color: {BLUE};'>✦ 𝓐𝓘 𝓕𝓲𝓽𝓷𝓮𝓼𝓼 𝓡𝓸𝓫𝓸𝓽: 𝓟𝓮𝓻𝓯𝓸𝓻𝓶𝓪𝓷𝓬𝓮 𝓞𝓷𝓫𝓸𝓪𝓻𝓭𝓲𝓷𝓰 ✦</h1>", unsafe_allow_html=True)

# --- SIDEBAR: INPUTS BIOMÉTRICOS ---
with st.sidebar:
    st.header("✦ User Biometrics")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=15, max_value=80, value=25)
    weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=75.0)
    height = st.number_input("Height (cm)", min_value=130, max_value=230, value=175)
    activity = st.select_slider(
        "Activity Level",
        options=["Sedentary", "Light", "Moderate", "Active", "Athlete"]
    )
    goal = st.radio("Primary Goal", ["Fat Loss (Cut)", "Maintenance", "Muscle Gain (Bulk)"])

# --- ENGINE: CÁLCULOS METABÓLICOS ---
# Mifflin-St Jeor Equation
s = 5 if gender == "Male" else -161
bmr = (10 * weight) + (6.25 * height) - (5 * age) + s

multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Athlete": 1.9}
tdee = bmr * multipliers[activity]

# Ajuste por Objetivo
if goal == "Fat Loss (Cut)":
    target_cal = tdee - 500
    p, c, f = 0.40, 0.35, 0.25 # High Protein for Cutting
elif goal == "Muscle Gain (Bulk)":
    target_cal = tdee + 300
    p, c, f = 0.25, 0.55, 0.20 # High Carb for Bulking
else:
    target_cal = tdee
    p, c, f = 0.30, 0.40, 0.30

# --- UI RENDER ---
c1, c2, c3 = st.columns(3)
c1.metric("BASAL METABOLIC RATE (BMR)", f"{bmr:.0f} kcal")
c2.metric("DAILY EXPENDITURE (TDEE)", f"{tdee:.0f} kcal")
c3.metric("TARGET DAILY CALORIES", f"{target_cal:.0f} kcal", delta=f"{target_cal - tdee:.0f}")

st.divider()

# Gráfico de Macros
labels = ['Protein', 'Carbs', 'Fats']
values = [(target_cal * p)/4, (target_cal * c)/4, (target_cal * f)/9]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=[AQUA, BLUE, "#FFFFFF"])])
fig.update_layout(title_text="✦ Daily Macro Distribution (Grams)", template="plotly_dark", paper_bgcolor="#0F0F0F")
st.plotly_chart(fig, use_container_width=True)

# Resumo para o Cliente (Summary Section)
st.markdown(f"### ✦ Execution Summary")
st.info(f"""
**Target:** {target_cal:.0f} Calories/Day. 
To reach your goal of **{goal}**, you must prioritize **{values[0]:.0f}g of Protein** to maintain lean mass and optimize recovery. 
Your metabolic baseline is set. Ready for Phase 2: Workout Architecture.

""")
