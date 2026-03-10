import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuração de Elite
st.set_page_config(page_title="Neural Nutrition | Alpha Fitness", layout="wide")

AQUA, BLUE = "#00FBFF", "#3D5AFE"

# Recuperação de Dados da Home
weight = st.session_state.get('user_weight', 80)
goal = st.session_state.get('user_goal', 'Maintenance')

st.markdown(f"<h1>✦ 𝓝𝓮𝓾𝓻𝓪𝓵 𝓝𝓾𝓽𝓻𝓲𝓽𝓲𝓸𝓷 𝓐𝓻𝓬𝓱𝓲𝓽𝓮𝓬𝓽 ✦</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Motor de Hidratação Alpha
# Base: 35ml por kg + Ajuste por fase
water_base = weight * 35 / 1000 
water_adjustment = 0.5 if goal in ["Cutting", "Bulking"] else 0.0
total_water = water_base + water_adjustment

c1, c2, c3 = st.columns(3)
c1.metric("ESTRATÉGIA ATUAL", goal.upper())
c2.metric("ALVO DE HIDRATAÇÃO", f"{total_water:.1f} Litros/Dia")
c3.info(f"💡 Dica Alpha: Beber 500ml de água mal acorde para ativar o metabolismo.")

# 3. Lógica de Nutrientes (Cálculos de Engenharia)
base_cals = 2500 if goal == "Maintenance" else 2800 if goal == "Bulking" else 2100
prot_total = weight * 2.2
fat_total = weight * 0.8
carb_total = (base_cals - (prot_total * 4) - (fat_total * 9)) / 4

with st.sidebar:
    st.header("✦ Protocolo")
    num_meals = st.slider("Número de Refeições", 3, 6, 4)

# 4. Base de Dados de Densidade (Macros por 100g de alimento cozinhado)
# [Nome, Prot, Carb, Fat]
food_data = {
    "Proteins": {"Frango Grelhado": 31, "Carne de Vaca (Patinho)": 28, "Ovos (3 unid)": 18, "Peixe Branco": 24, "Whey Protein": 25},
    "Carbs": {"Arroz Basmati": 28, "Batata Doce": 20, "Aveia": 60, "Massa Integral": 25, "Fruta Variada": 15},
    "Fats": {"Abacate": 15, "Azeite de Oliva (10ml)": 10, "Frutos Secos": 50, "Manteiga de Amendoim": 50}
}

# 5. Meal Architect (Geração de Plano Detalhado)
st.subheader("✦ Plano de Refeições Detalhado")

# Divisão por refeição
p_meal, c_meal, f_meal = prot_total/num_meals, carb_total/num_meals, fat_total/num_meals

# Estrutura de Refeições Dinâmicas
meal_templates = [
    {"title": "Pequeno-Almoço (Despertar Metabólico)", "p_source": "Ovos (3 unid)", "c_source": "Aveia"},
    {"title": "Almoço (Performance Lunch)", "p_source": "Frango Grelhado", "c_source": "Arroz Basmati"},
    {"title": "Lanche (Nutrient Timing)", "p_source": "Whey Protein", "c_source": "Fruta Variada"},
    {"title": "Jantar (Recovery Dinner)", "p_source": "Peixe Branco", "c_source": "Batata Doce"},
    {"title": "Ceia / Snack Extra", "p_source": "Carne de Vaca (Patinho)", "c_source": "Massa Integral"}
]

meal_cols = st.columns(2)
for i in range(num_meals):
    template = meal_templates[i % len(meal_templates)]
    with meal_cols[i % 2]:
        with st.expander(f"REFEIÇÃO {i+1} - {template['title']}", expanded=True):
            # Cálculo de quantidades em gramas
            p_qty = (p_meal / food_data["Proteins"][template['p_source']]) * 100
            c_qty = (c_meal / food_data["Carbs"][template['c_source']]) * 100
            
            st.markdown(f"""
            **Lista de Compras (Quantidades Cozinhadas):**
            * 🟢 **{p_qty:.0f}g** de {template['p_source']}
            * 🔵 **{c_qty:.0f}g** de {template['c_source']}
            * ⚪ **{f_meal:.0f}g** de Gordura (ex: 1 colher de Azeite ou Abacate)
            
            **Macros da Refeição:**
            `P: {p_meal:.1f}g | C: {c_meal:.1f}g | F: {f_meal:.1f}g`
            """)

# 6. Gráfico de Alvos Totais
fig = go.Figure(data=[
    go.Bar(name='Proteína', x=['Total'], y=[prot_total], marker_color=AQUA),
    go.Bar(name='Carbos', x=['Total'], y=[carb_total], marker_color=BLUE),
    go.Bar(name='Gorduras', x=['Total'], y=[fat_total], marker_color='#FFFFFF')
])
fig.update_layout(barmode='group', template="plotly_dark", height=300, paper_bgcolor="#0F0F0F", plot_bgcolor="#0F0F0F")
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("### ✦ ALPHA MISSION SUMMARY")
st.code(f"""
PROTOCOLO: {goal.upper()}
HIDRATAÇÃO: {total_water:.1f}L / DIA
FREQUÊNCIA: {num_meals} JANELAS DE ALIMENTAÇÃO
STATUS: MOTOR NUTRICIONAL EM EXECUÇÃO
""", language="text")
