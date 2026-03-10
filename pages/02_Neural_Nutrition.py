import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Configuração de Autoridade Alpha
st.set_page_config(page_title="Neural Nutrition | Alpha Fitness", layout="wide")

# Identidade Visual
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

# 2. Sincronização de Dados (Session State)
weight = st.session_state.get('user_weight', 80.0)
goal = st.session_state.get('user_goal', 'Maintenance')

st.markdown(f"<h1>✦ 𝓝𝓮𝓾𝓻𝓪𝓵 𝓝𝓾𝓽𝓻𝓲𝓽𝓲𝓸𝓷 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 3. Hidratação e Status Biométrico
water_target = (weight * 35 / 1000) + (0.5 if goal != "Maintenance" else 0.0)

c1, c2, c3 = st.columns(3)
c1.metric("ESTRATÉGIA ATUAL", goal.upper())
c2.metric("ALVO DE HIDRATAÇÃO", f"{water_target:.1f} Litros/Dia")
c3.info(f"💡 Dica Alpha: Beber 500ml de água fria ao acordar para otimizar a TMB.")

# 4. Engenharia de Macros (Cálculos de Precisão)
# Definição calórica baseada no objetivo
if goal == "Bulking": base_cals = 2800
elif goal == "Cutting": base_cals = 2000
else: base_cals = 2500

p_total = weight * 2.2
f_total = weight * 0.8
c_total = (base_cals - (p_total * 4) - (f_total * 9)) / 4

with st.sidebar:
    st.header("✦ Protocolo")
    num_meals = st.slider("Janelas de Alimentação", 3, 6, 4)

p_meal, c_meal, f_meal = p_total/num_meals, c_total/num_meals, f_total/num_meals

# 5. Database de Densidade Nutricional (Macro por 100g ou Unidade)
db = {
    "P": {"Frango": 31, "Vaca (Patinho)": 28, "Peixe Branco": 24, "Whey": 80, "Ovos (unid)": 6, "Claras (ml)": 11, "Iogurte Grego": 10},
    "C": {"Arroz": 28, "Batata Doce": 20, "Aveia": 60, "Massa Integral": 25, "Fruta": 15, "Pão Integral": 45, "Granola": 65},
    "F": {"Azeite (ml)": 100, "Abacate": 15, "Manteiga Amendoim": 50, "Frutos Secos": 50}
}

# 6. Cardápio Gourmet (3 Opções Únicas por Categoria)
meal_options = {
    "DESJEJUM (Morning Fuel)": [
        {"name": "Opção A: Alpha Pancakes", "p": "Claras (ml)", "c": "Aveia", "f": "Manteiga Amendoim"},
        {"name": "Opção B: Omelete Mediterrânea", "p": "Ovos (unid)", "c": "Pão Integral", "f": "Abacate"},
        {"name": "Opção C: Power Yogurt Bowl", "p": "Iogurte Grego", "c": "Granola", "f": "Frutos Secos"}
    ],
    "SÓLIDA (Performance Meal)": [
        {"name": "Opção A: Classic Gains", "p": "Frango", "c": "Arroz", "f": "Azeite (ml)"},
        {"name": "Opção B: Red Power", "p": "Vaca (Patinho)", "c": "Batata Doce", "f": "Azeite (ml)"},
        {"name": "Opção C: Lean Marine", "p": "Peixe Branco", "c": "Massa Integral", "f": "Azeite (ml)"}
    ],
    "SNACK (Metabolic Bridge)": [
        {"name": "Opção A: Anabolic Shake", "p": "Whey", "c": "Fruta", "f": "Frutos Secos"},
        {"name": "Opção B: Deli Toast", "p": "Frango", "c": "Pão Integral", "f": "Abacate"},
        {"name": "Opção C: Energy Mix", "p": "Iogurte Grego", "c": "Aveia", "f": "Manteiga Amendoim"}
    ]
}

# 7. Renderização do Sistema de Escolhas
st.subheader("✦ Gestão de Refeições Personalizada")

cols = st.columns(2)
for i in range(num_meals):
    # Lógica de Categorização das Refeições
    if i == 0: 
        m_type = "DESJEJUM (Morning Fuel)"
    elif i == num_meals - 1 or (i == 1 and num_meals > 3): 
        m_type = "SÓLIDA (Performance Meal)"
    else: 
        m_type = "SNACK (Metabolic Bridge)"
    
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"#### REFEIÇÃO {i+1}")
            st.caption(f"Tipo: {m_type}")
            
            # Selectbox de Opção Gourmet
            choice = st.selectbox("Escolha o seu menu:", 
                                [opt["name"] for opt in meal_options[m_type]], 
                                key=f"meal_v35_idx_{i}")
            
            selected_opt = next(opt for opt in meal_options[m_type] if opt["name"] == choice)
            
            # Cálculos Dinâmicos de Peso/Quantidade
            if "unid" in selected_opt['p']:
                p_display = f"{max(1, p_meal / db['P'][selected_opt['p']]):.0f} unid"
            else:
                p_display = f"{(p_meal / db['P'][selected_opt['p']]) * 100:.0f}g/ml"
            
            c_display = f"{(c_meal / db['C'][selected_opt['c']]) * 100:.0f}g"
            
            if "ml" in selected_opt['f']:
                f_display = f"{f_meal:.0f}ml"
            else:
                f_display = f"{(f_meal / db['F'][selected_opt['f']]) * 100:.0f}g"
            
            # UI Card de Ingredientes
            st.markdown(f"""
            <div style="background-color: #161616; padding: 15px; border-radius: 10px; border-left: 5px solid {AQUA};">
                <p style="margin:0; color: #FFF;">🟢 <b>{p_display}</b> de {selected_opt['p']}</p>
                <p style="margin:0; color: #FFF;">🔵 <b>{c_display}</b> de {selected_opt['c']}</p>
                <p style="margin:0; color: #FFF;">⚪ <b>{f_display}</b> de {selected_opt['f']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<p style='font-size:12px; color:#888; margin-top:10px;'>Target Macros: {p_meal:.0f}P | {c_meal:.0f}C | {f_meal:.0f}F</p>", unsafe_allow_html=True)

# 8. Gráfico de Alvos Macro
st.divider()
st.subheader("✦ Daily Macro Distribution")
fig = go.Figure(data=[
    go.Pie(labels=['Proteína', 'Carbos', 'Gorduras'], 
           values=[p_total*4, c_total*4, f_total*9],
           hole=.5,
           marker_colors=[AQUA, BLUE, "#FFFFFF"])
])
fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="#0F0F0F")
st.plotly_chart(fig, use_container_width=True)

# 9. Rodapé de Missão
st.divider()
st.markdown("### ✦ MISSION EXECUTION PROTOCOL")
st.code(f"USER: {weight}KG | GOAL: {goal.upper()} | STATUS: OPTIMIZED", language="text")
