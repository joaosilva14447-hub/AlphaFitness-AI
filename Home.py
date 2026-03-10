import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Configuração Master Alpha
st.set_page_config(page_title="Neural Nutrition | Alpha Fitness", layout="wide")

AQUA, BLUE = "#00FBFF", "#3D5AFE"

# Recuperação de Dados Inteligente
weight = st.session_state.get('user_weight', 80)
goal = st.session_state.get('user_goal', 'Maintenance')

st.markdown(f"<h1>✦ 𝓝𝓮𝓾𝓻𝓪𝓵 𝓝𝓾𝓽𝓻𝓲𝓽𝓲𝓸𝓷 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Motor de Hidratação Estratégica
water_base = weight * 35 / 1000 
water_adjustment = 0.5 if goal in ["Cutting", "Bulking"] else 0.0
total_water = water_base + water_adjustment

c1, c2, c3 = st.columns(3)
c1.metric("ESTRATÉGIA", goal.upper())
c2.metric("HIDRATAÇÃO DIÁRIA", f"{total_water:.1f} Litros")
c3.info(f"💧 Fase: {goal}. Beber 500ml de água fria em jejum para termogénese.")

# 3. Engenharia de Macros
base_cals = 2500 if goal == "Maintenance" else 2800 if goal == "Bulking" else 2100
prot_total = weight * 2.2
fat_total = weight * 0.8
carb_total = (base_cals - (prot_total * 4) - (fat_total * 9)) / 4

with st.sidebar:
    st.header("✦ Protocolo de Execução")
    num_meals = st.slider("Número de Refeições", 3, 6, 4)

p_meal, c_meal, f_meal = prot_total/num_meals, carb_total/num_meals, fat_total/num_meals

# 4. Base de Dados de Alimentos (Macro por 100g)
db = {
    "P": {"Ovos (unid)": 6, "Claras (ml)": 11, "Frango": 31, "Vaca": 28, "Peixe": 24, "Whey": 80, "Iogurte Grego": 10},
    "C": {"Aveia": 60, "Arroz": 28, "Batata Doce": 20, "Massa": 25, "Fruta": 15, "Pão Integral": 45, "Granola": 65},
    "F": {"Azeite (ml)": 100, "Abacate": 15, "Manteiga Amendoim": 50, "Frutos Secos": 50}
}

# 5. Dicionário de Opções Gourmet (Harmonizadas)
# Estrutura: {Tipo: [ {Opção 1}, {Opção 2}, {Opção 3} ] }
meal_options = {
    "Desjejum": [
        {"name": "Pancakes de Aveia", "p": "Claras (ml)", "c": "Aveia", "f": "Manteiga Amendoim"},
        {"name": "Omelete Alpha", "p": "Ovos (unid)", "c": "Pão Integral", "f": "Abacate"},
        {"name": "Power Bowl", "p": "Iogurte Grego", "c": "Granola", "f": "Frutos Secos"}
    ],
    "Principal": [
        {"name": "Classic Gainz", "p": "Frango", "c": "Arroz", "f": "Azeite (ml)"},
        {"name": "Red Meat Performance", "p": "Vaca", "c": "Batata Doce", "f": "Azeite (ml)"},
        {"name": "Lean Marine", "p": "Peixe", "c": "Massa", "f": "Azeite (ml)"}
    ],
    "Snack": [
        {"name": "Alpha Shake", "p": "Whey", "c": "Fruta", "f": "Frutos Secos"},
        {"name": "Sandwich Proteico", "p": "Frango", "c": "Pão Integral", "f": "Abacate"},
        {"name": "Yogurt Mix", "p": "Iogurte Grego", "c": "Aveia", "f": "Manteiga Amendoim"}
    ]
}

# 6. Renderização das Refeições
st.subheader("✦ Gestão de Refeições (Escolha 1 opção por horário)")

for i in range(num_meals):
    # Determinar tipo de refeição baseado na ordem
    if i == 0: m_type = "Desjejum"
    elif i == num_meals - 1 or i == 1: m_type = "Principal"
    else: m_type = "Snack"
    
    with st.expander(f"REFEIÇÃO {i+1} - {m_type.upper()}", expanded=True):
        t1, t2, t3 = st.tabs(["Opção A", "Opção B", "Opção C"])
        
        for idx, tab in enumerate([t1, t2, t3]):
            opt = meal_options[m_type][idx]
            with tab:
                # Cálculos de Quantidade (Gramas/ML/Unid)
                if "unid" in opt['p']: p_qty = max(1, p_meal / db['P'][opt['p']])
                else: p_qty = (p_meal / db['P'][opt['p']]) * 100
                
                c_qty = (c_meal / db['C'][opt['c']]) * 100
                f_qty = (f_meal / db['F'][opt['f']]) * 100 if "ml" not in opt['f'] else f_meal
                
                st.markdown(f"#### {opt['name']}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Ingredientes:**")
                    st.write(f"- 🟢 {p_qty:.0f}{' unid' if 'unid' in opt['p'] else 'g/ml'} de **{opt['p']}**")
                    st.write(f"- 🔵 {c_qty:.0f}g de **{opt['c']}**")
                    st.write(f"- ⚪ {f_qty:.0f}{'ml' if 'ml' in opt['f'] else 'g'} de **{opt['f']}**")
                
                with col_b:
                    st.write("**Target Macros:**")
                    st.code(f"P: {p_meal:.1f}g | C: {c_meal:.1f}g | F: {f_meal:.1f}g")

# 7. Gráfico de Performance Semanal
st.divider()
st.subheader("✦ Macronutrient Distribution")
fig = go.Figure(data=[
    go.Bar(name='Proteína', x=['Total'], y=[prot_total], marker_color=AQUA),
    go.Bar(name='Carbos', x=['Total'], y=[carb_total], marker_color=BLUE),
    go.Bar(name='Gorduras', x=['Total'], y=[fat_total], marker_color='#FFFFFF')
])
fig.update_layout(template="plotly_dark", height=300, paper_bgcolor="#0F0F0F", plot_bgcolor="#0F0F0F")
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### ✦ MISSION EXECUTION PROTOCOL")
st.code(f"PROTOCOLO: {goal} | HIDRATAÇÃO: {total_water:.1f}L | STATUS: OPTIMIZED", language="text")

