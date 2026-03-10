import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Configuração de Autoridade
st.set_page_config(page_title="Neural Nutrition | Alpha Fitness", layout="wide")

AQUA, BLUE = "#00FBFF", "#3D5AFE"

# Recuperação Segura de Dados
weight = st.session_state.get('user_weight', 80)
goal = st.session_state.get('user_goal', 'Maintenance')

st.markdown(f"<h1 style='text-align: center; color: {BLUE};'>✦ 𝓝𝓮𝓾𝓻𝓪𝓵 𝓝𝓾𝓽𝓻𝓲𝓽𝓲𝓸𝓷 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Hidratação Estratégica (Cálculo em Tempo Real)
water_target = (weight * 35 / 1000) + (0.5 if goal != "Maintenance" else 0.0)

c1, c2, c3 = st.columns(3)
c1.metric("ESTRATÉGIA", goal.upper())
c2.metric("HIDRATAÇÃO", f"{water_target:.1f} Litros")
c3.info(f"💡 Dica: Beber 500ml de água fria ao acordar para termogênese.")

# 3. Engenharia de Macros (Cálculos de Precisão)
base_cals = 2500 if goal == "Maintenance" else 2800 if goal == "Bulking" else 2000
p_total = weight * 2.2
f_total = weight * 0.8
c_total = (base_cals - (p_total * 4) - (f_total * 9)) / 4

with st.sidebar:
    st.header("✦ Protocolo")
    num_meals = st.slider("Refeições", 3, 6, 4)

p_meal, c_meal, f_meal = p_total/num_meals, c_total/num_meals, f_total/num_meals

# 4. Database de Densidade Alpha
db = {
    "P": {"Frango": 31, "Vaca (Patinho)": 28, "Peixe Branco": 24, "Whey": 80, "Ovos (unid)": 6, "Claras (ml)": 11, "Iogurte Grego": 10},
    "C": {"Arroz": 28, "Batata Doce": 20, "Aveia": 60, "Massa Integral": 25, "Fruta": 15, "Pão Integral": 45, "Granola": 65},
    "F": {"Azeite (ml)": 100, "Abacate": 15, "Manteiga Amendoim": 50, "Frutos Secos": 50}
}

# 5. Cardápio Gourmet Harmonizado
meal_options = {
    "DESJEJUM": [
        {"name": "Opção A: Omelete Alpha", "p": "Ovos (unid)", "c": "Pão Integral", "f": "Abacate"},
        {"name": "Opção B: Pancakes Proteicas", "p": "Claras (ml)", "c": "Aveia", "f": "Manteiga Amendoim"},
        {"name": "Opção C: Power Yogurt Bowl", "p": "Iogurte Grego", "c": "Granola", "f": "Frutos Secos"}
    ],
    "ALMOÇO/JANTAR": [
        {"name": "Opção A: Classic Gains", "p": "Frango", "c": "Arroz", "f": "Azeite (ml)"},
        {"name": "Opção B: Red Performance", "p": "Vaca (Patinho)", "c": "Batata Doce", "f": "Azeite (ml)"},
        {"name": "Opção C: Lean Marine", "p": "Peixe Branco", "c": "Massa Integral", "f": "Azeite (ml)"}
    ],
    "SNACK": [
        {"name": "Opção A: Alpha Shake", "p": "Whey", "c": "Fruta", "f": "Frutos Secos"},
        {"name": "Opção B: Toast Proteico", "p": "Frango", "c": "Pão Integral", "f": "Abacate"},
        {"name": "Opção C: Mix Energético", "p": "Iogurte Grego", "c": "Aveia", "f": "Manteiga Amendoim"}
    ]
}

# 6. Renderização de Refeições com Sistema de Seleção
st.subheader("✦ Gestão de Janelas de Alimentação")

user_selections = []

cols = st.columns(2)
for i in range(num_meals):
    # Lógica de tipo de refeição
    if i == 0: m_type = "DESJEJUM"
    elif i == num_meals - 1 or i == 1: m_type = "ALMOÇO/JANTAR"
    else: m_type = "SNACK"
    
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"#### REFEIÇÃO {i+1} ({m_type})")
            
            # Seleção de Opção (Key única baseada no index para não dar erro)
            choice = st.selectbox("Escolha sua opção:", 
                                [opt["name"] for opt in meal_options[m_type]], 
                                key=f"meal_{i}")
            
            # Encontrar dados da opção escolhida
            selected_opt = next(opt for opt in meal_options[m_type] if opt["name"] == choice)
            
            # Cálculos de Quantidade
            if "unid" in selected_opt['p']: p_val = f"{max(1, p_meal / db['P'][selected_opt['p']]):.0f} unid"
            else: p_val = f"{(p_meal / db['P'][selected_opt['p']]) * 100:.0f}g/ml"
            
            c_val = f"{(c_meal / db['C'][selected_opt['c']]) * 100:.0f}g"
            f_val = f"{f_meal if 'ml' in selected_opt['f'] else (f_meal / db['F'][selected_opt['f']]) * 100:.0f}{'ml' if 'ml' in selected_opt['f'] else 'g'}"
            
            # Display dos Ingredientes
            st.markdown(f"""
            - 🟢 **{p_val}** de {selected_opt['p']}
            - 🔵 **{c_val}** de {selected_opt['c']}
            - ⚪ **{f_val}** de {selected_opt['f']}
            """)
            st.caption(f"Target: {p_meal:.0f}P | {c_meal:.0f}C | {f_meal:.0f}F")

# 7. Gráfico de Alvos Totais
st.divider()
st.subheader("✦ Macronutrient Target Distribution")
fig = go.Figure(data=[
    go.Pie(labels=['Proteína', 'Carbos', 'Gorduras'], 
           values=[p_total*4, c_total*4, f_total*9],
           hole=.5,
           marker_colors=[AQUA, BLUE, "#FFFFFF"])
])
fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="#0F0F0F")
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### ✦ MISSION EXECUTION PROTOCOL")
st.code(f"USER: {weight}KG | GOAL: {goal} | STATUS: OPTIMIZED", language="text")
